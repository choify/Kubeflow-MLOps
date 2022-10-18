import io
import boto3
import numpy as np
import pandas as pd
from mlflow import MlflowClient


def load_data_from_s3() -> pd.DataFrame:
    """
    load data from amazon s3, using credential by env
    Args:
        None
    Returns:
        loaded data as pandas.DataFrame
    """
    with open("data/yellow_tripdata_2017-01.parquet.dvc", "r") as f:
        file = f.readlines()
    md5 = file[1].split(" ")[-1][:-1]

    s3_client = boto3.client(
        "s3",
    )
    BUCKET_NAME = "hajong-data"
    object_key = "/".join(["data", md5[:2], md5[2:]])
    object_ = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_key)
    print(
        "*" * 40,
        f"Bucket name: {BUCKET_NAME} \nObject key: {object_key}",
        "*" * 40,
        sep="\n",
    )
    df = pd.read_parquet(io.BytesIO(object_["Body"].read()))
    return df


def reduce_mem_usage(df: pd.DataFrame) -> pd.DataFrame:
    """iterate through all the columns of a dataframe and modify the data type
    to reduce memory usage.
    Args:
        df: pandas.DataFrame
    Retruns:
        memory reduced DataFrame
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print("Memory usage of dataframe is {:.2f} MB".format(start_mem))

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype("category")

    end_mem = df.memory_usage().sum() / 1024**2
    print("Memory usage after optimization is: {:.2f} MB".format(end_mem))
    print("Decreased by {:.1f}%".format(100 * (start_mem - end_mem) / start_mem))
    return df


def preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    """
    return preprocessed data by using drop cols, making new cols etc.
    Args:
        data: data to preprocess
    Returns:
        preporcessed data as pandas.DataFrame
    """
    data.drop(
        [
            "VendorID",
            "store_and_fwd_flag",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "total_amount",
            "congestion_surcharge",
            "airport_fee",
        ],
        axis=1,
        inplace=True,
    )
    ol = data.loc[(data.fare_amount > 500000)].index
    data.drop(ol, inplace=True)
    data["drive_time_diff"] = (
        data["tpep_dropoff_datetime"] - data["tpep_pickup_datetime"]
    ) / np.timedelta64(1, "s")
    data.drop(columns=["tpep_dropoff_datetime", "tpep_pickup_datetime"], inplace=True)
    # category_cols = ["RatecodeID", "PULocationID", "DOLocationID", "payment_type"]
    # for col in category_cols:
    #     data[col] = data[col].astype("category")
    data.dropna(axis=0, inplace=True)
    return data


def rename_model_on_s3() -> None:
    mlflow_client = MlflowClient("http://13.124.36.34:5000/")
    run_info = mlflow_client.search_runs("0")[0]
    run_id = run_info.info.run_id
    s3_client = boto3.client(
        "s3",
    )
    BUCKET_NAME = "hajong-data"
    old_file_key = "mlflow/mlflow/artifacts/0/" + run_id + "/artifacts/model/model.xgb"
    new_file_key = "mlflow/mlflow/artifacts/0/" + run_id + "/artifacts/model/model.bst"
    s3_client.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={"Bucket": BUCKET_NAME, "Key": old_file_key},
        Key=new_file_key,
    )
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=old_file_key)
