#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  PYTHON=python
fi

prompt=""
while true; do
  if ! read -r -p "Enter your prompt (press ENTER to ask again): " prompt; then
    exit 0
  fi
  if [ -z "$prompt" ]; then
    continue
  fi
  break
done

exec "$PYTHON" "$SCRIPT_DIR/main.py" "$prompt"
