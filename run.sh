#!/bin/bash
set -e
python scripts/run_demo.py
uvicorn backend.main:app --host 127.0.0.1 --port 8000 & echo $! > .backend.pid
(cd frontend && npm run dev -- --port 5173) & echo $! > .frontend.pid
wait
