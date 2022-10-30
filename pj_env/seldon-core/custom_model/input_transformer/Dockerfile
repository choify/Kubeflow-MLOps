FROM python:3.7
RUN mkdir /home/app && chmod -R 777 /home/app

COPY ./InputTransformer.py /home/app/InputTransformer.py
ADD taxi_zone /home/app/taxi_zone
WORKDIR /home/app

EXPOSE 9000

ENV MODEL_NAME InputTransformer
ENV SERVICE_TYPE TRANSFORMER

RUN pip install seldon-core==1.6.0 markupsafe==2.0.1 geopandas

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE 