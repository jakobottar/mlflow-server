#!/bin/bash

mlflow server \
    --host 0.0.0.0 \
    --default-artifact-root "./mlruns" \
    --port 5000