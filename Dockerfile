FROM python:3.10

WORKDIR /mlflow

RUN mkdir -p /mlflow/mlruns \
    && pip install mlflow

COPY run.sh /mlflow/run.sh

EXPOSE 5000

CMD ["/mlflow/run.sh"]