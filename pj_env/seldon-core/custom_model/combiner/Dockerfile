FROM python:3.7
RUN mkdir /home/app && chmod -R 777 /home/app

COPY ./Combiner.py /home/app/Combiner.py
WORKDIR /home/app

EXPOSE 9000

ENV MODEL_NAME Combiner
ENV SERVICE_TYPE COMBINER

RUN pip install numpy==1.18.5 seldon-core==1.6.0 markupsafe==2.0.1

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE 