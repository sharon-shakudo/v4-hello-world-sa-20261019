#!/usr/bin/env bash
set -euo pipefail
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8787}"
exec python3 -u app.py
