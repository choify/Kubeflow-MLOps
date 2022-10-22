import argparse
import xgboost as xgb
from sklearn.model_selection import train_test_split
from mlflow import MlflowClient


from utils import load_data_from_s3, reduce_mem_usage, load_model_from_s3


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--eta", type=float, default=0.3)
    parser.add_argument("--gamma", type=float, default=0)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--min-child-weight", type=float, default=1)
    parser.add_argument("--subsample", type=float, default=1.0)
    parser.add_argument("--colsample-bytree", type=float, default=1.0)
    parser.add_argument("--reg-alpha", type=float, default=0)
    parser.add_argument("--reg-lambda", type=float, default=1.0)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    data = reduce_mem_usage(load_data_from_s3())
    y = data.pop("fare_amount")
    X = data.copy()
    del data

    train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size=0.2)

    dtrain = xgb.DMatrix(train_X, train_y)
    dvalid = xgb.DMatrix(valid_X, valid_y)

    # specify parameters via map
    param = {
        "eta": args.eta,
        "gamma": args.gamma,
        "max_depth": args.max_depth,
        "min_child_weight": args.min_child_weight,
        "subsample": args.subsample,
        "colsample_bytree": args.colsample_bytree,
        "reg_alpha": args.reg_alpha,
        "reg_lambda": args.reg_lambda,
        "objective": "reg:squarederror",
    }

    mlflow_client = MlflowClient("http://13.124.36.34:5000/")
    if len(mlflow_client.search_runs("0")) == 0:
        bst = xgb.train(
            param,
            dtrain,
            num_boost_round=2000,
            evals=[(dtrain, "Train"), (dvalid, "Validation")],
            early_stopping_rounds=100,
        )
    else:
        print("older model loaded from s3 ...")
        model = load_model_from_s3()
        bst = xgb.train(
            param,
            dtrain,
            num_boost_round=2000,
            evals=[(dtrain, "Train"), (dvalid, "Validation")],
            early_stopping_rounds=100,
            xgb_model=model,
        )
