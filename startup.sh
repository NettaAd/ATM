#!/bin/bash

# Launch FastAPI using Uvicorn on port 8000
exec uvicorn main:app --host=0.0.0.0 --port=8000
