#!/bin/bash
set -e

if [ -z "$RUNNER_REPOSITORY_URL" ] || [ -z "$RUNNER_TOKEN" ]; then
  echo "Missing RUNNER_REPOSITORY_URL or RUNNER_TOKEN"
  exit 1
fi

if [ ! -f .runner ]; then
  ./config.sh \
    --url "$RUNNER_REPOSITORY_URL" \
    --token "$RUNNER_TOKEN" \
    --name "${RUNNER_NAME:-default}" \
    --unattended \
    --replace
fi

trap './config.sh remove --unattended --token "$RUNNER_TOKEN"' EXIT

./run.sh
