#!/bin/bash

echo "upgrading db..."
mlflow db upgrade postgresql+psycopg2://${DB_USER}:${DB_PASSWD}@${DB_HOST}/${DB_NAME}

# backend is relative to server
# artifact is relative to run
echo "launching mlflow tracking server..."
mlflow server \
    --backend-store-uri postgresql+psycopg2://${DB_USER}:${DB_PASSWD}@${DB_HOST}/${DB_NAME} \
    --default-artifact-root ${ARTIFACT_ROOT} \
    --host 0.0.0.0