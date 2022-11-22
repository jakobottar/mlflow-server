#!/bin/bash

echo "launching mlflow tracking server..."

# backend is relative to server
# artifact is relative to run
mlflow server \
    --host 0.0.0.0 \
    --backend-store-uri "./backend" \
    --port 5000