#!/bin/sh

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 80 embrapa.app:app
