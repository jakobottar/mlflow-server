FROM python:3.10

WORKDIR /data

# psycopg2 is needed for postgresql, boto3 for s3
RUN mkdir -p /data/backend \
    && pip install mlflow psycopg2 boto3

COPY run.sh /data/run.sh

CMD bash run.sh
