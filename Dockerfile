FROM python:3.10

WORKDIR /data

# psycopg2 is needed for postgresql 
# pysftp is needed for sftp
RUN mkdir -p /data/backend \
    && pip install mlflow psycopg2 pysftp

COPY run.sh /data/run.sh

EXPOSE 5000

ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_NAME mlflowdb
ENV DB_USER "$POSTGRES_USER"
ENV DB_PASSWD "$POSTGRES_PASSWORD"
ENV USERNAME "$SFTP_USERNAME"
ENV PASSWORD "$SFTP_PASSWORD"
ENV ARTIFACT_ROOT sftp://${USERNAME}:${PASSWORD}@tularosa.sci.utah.edu/data/

CMD bash run.sh
