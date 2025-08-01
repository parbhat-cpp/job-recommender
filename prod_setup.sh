#!/bin/bash

echo "Setting prod environment"

python src/pipeline/__init__.py

echo "Starting uvicorn..."

uvicorn app:app --host 0.0.0.0 --port 8000
