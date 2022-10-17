import argparse
import xgboost as xgb
from sklearn.model_selection import train_test_split

# import mlflow

from utils import load_data_from_s3, preprocessing, reduce_mem_usage


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

    data = reduce_mem_usage(preprocessing(load_data_from_s3()))
    y = data.pop("fare_amount")
    X = data.copy()
    del data

    train_X, valid_X, train_y, valid_y = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # mlflow.xgboost.autolog(log_input_examples=True)
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
    bst = xgb.train(
        param,
        dtrain,
        num_boost_round=2000,
        evals=[(dtrain, "Train"), (dvalid, "Validation")],
        early_stopping_rounds=100,
    )
