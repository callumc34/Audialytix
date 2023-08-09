#!/bin/bash
uvicorn server:app --reload --port $PORT --host 0.0.0.0 --log-level info
