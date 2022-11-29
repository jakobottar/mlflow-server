FROM python:3.10

WORKDIR /data

# psycopg2 is needed for postgresql 
RUN mkdir -p /data/backend \
    && pip install mlflow psycopg2

COPY run.sh /data/run.sh

EXPOSE 5000

ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_NAME mlflowdb
ENV DB_USER mlflow
ENV DB_PASSWD ilovekittens1234
ENV ARTIFACT_ROOT ./mlruns/

CMD bash run.sh
