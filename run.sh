#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  PYTHON=python
fi

prompt=""
read -r -p "Enter your prompt: " prompt

if [ -z "$prompt" ]; then
  echo "Error: prompt cannot be empty." >&2
  exit 1
fi

exec "$PYTHON" "$SCRIPT_DIR/main.py" "$prompt"
