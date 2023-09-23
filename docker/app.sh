#!/bin/bash

#alembic upgrade head

cd app

uvicorn --host 0.0.0.0 --port 8000 main:app
