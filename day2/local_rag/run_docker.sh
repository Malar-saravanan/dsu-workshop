#!/usr/bin/env bash
# Build and run the RAG app container.
# Injects secrets/config at runtime via --env-file (never copied into the image).
set -euo pipefail

cd "$(dirname "$0")"
IMAGE="${IMAGE:-rag-app}"

# Prefer local_rag1/.env
if [[ -n "${ENV_FILE:-}" ]]; then
  :
elif [[ -f ".env" ]]; then
  ENV_FILE=".env"
elif [[ -f "../.env" ]]; then
  ENV_FILE="../.env"
else
  echo "ERROR: no .env found."
  echo "Create local_rag1/.env from .env.example"
  exit 1
fi

echo "Using env file: $ENV_FILE"

docker build -t "$IMAGE" .
docker run --rm --env-file "$ENV_FILE" -p 7860:7860 "$IMAGE"
