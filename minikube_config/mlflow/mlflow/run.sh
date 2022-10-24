#!/bin/sh

set -e

export MLFLOW_BACKEND_STORE_URI='postgresql://mlflow:mlflow@postgresql-mlflow-service.mlflow-system.svc.cluster.local:5432/mlflow'


echo ${MLFLOW_BACKEND_STORE_URI}
echo ${PORT}

mlflow server \
    --backend-store-uri $MLFLOW_BACKEND_STORE_URI \
    --default-artifact-root S3://team06/mlflow/mlflow/artifacts \
    --host 0.0.0.0 \
    --port $PORT