FROM python:3.7-slim-buster
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends build-essential libpq-dev
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
WORKDIR /app
RUN mkdir data
COPY data/train_data.parquet.dvc data/
COPY xgb.py .
COPY utils.py .
RUN sed -i '9a\import datetime' /usr/local/lib/python3.7/site-packages/xgboost/callback.py
RUN sed -i '498a\            msg = datetime.datetime.now().isoformat("T")[:-7] + "Z " + msg' /usr/local/lib/python3.7/site-packages/xgboost/callback.py