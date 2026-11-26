#!/bin/bash
set -e
python scripts/run_demo.py
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
BACK=$!
trap 'kill $BACK 2>/dev/null || true' EXIT
sleep 2
if command -v npm >/dev/null 2>&1; then (cd frontend && npm install --silent && npm run dev -- --port 5173); else echo 'Backend demo ready; install Node.js 18+ to launch frontend.'; fi
