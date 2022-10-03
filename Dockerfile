FROM python:3.9-slim-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY train.py .
CMD ["python", "train.py"]