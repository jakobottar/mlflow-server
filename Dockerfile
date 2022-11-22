FROM python:3.10

WORKDIR /data

RUN mkdir -p /data/backend \
    && pip install mlflow

VOLUME ["/data/backend"]

COPY run.sh /data/run.sh

EXPOSE 5000

CMD ["/data/run.sh"]