FROM python:3.7-slim-buster


# Build dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends build-essential libpq-dev

ENV PORT 5000

EXPOSE $PORT

RUN mkdir -p /tmp/mlflow
ENV MLFLOW_BACKEND_STORE_URI file:///tmp/mlflow 

RUN mkdir -p /opt/mlflow

ARG MLFLOW_VERSION=1.29.0
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir mlflow==$MLFLOW_VERSION boto3 psycopg2-binary

COPY run.sh /opt/mlflow
RUN chmod -R 777 /opt/mlflow/

ENTRYPOINT ["/opt/mlflow/run.sh"]