FROM python:3.10

WORKDIR /data

RUN mkdir -p /data/backend \
    && pip install mlflow

VOLUME ["/data/backend"]

COPY run.sh /data/run.sh

EXPOSE 5000

ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_NAME mlflowdb
ENV DB_USER mlflow
ENV DB_PASSWD ilovekittens1234
ENV ARTIFACT_ROOT ./mlruns/

CMD mlflow server --backend-store-uri postgresql+psycopg2://${DB_USER}:${DB_PASSWD}@${DB_HOST}/${DB_NAME} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0