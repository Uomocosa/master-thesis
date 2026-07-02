#!/usr/bin/env bash
set -euo pipefail

# Prevent MSYS (Git Bash on Windows) from mangling paths like /workdir.
export MSYS_NO_PATHCONV=1

IMAGE="thesis-builder:latest"
# Resolve the repo root regardless of where the script is called from.
CONTEXT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# -------------------------------------------------------------------
# On Windows (MSYS/MINGW/CYGWIN) and macOS, Podman needs a VM.
# Start it if it is not already running.
# -------------------------------------------------------------------
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*|Darwin)
    if ! podman machine list --format '{{.Running}}' 2>/dev/null | grep -qi 'true'; then
      echo ">> Starting Podman machine..."
      podman machine start
    fi
    ;;
esac

# -------------------------------------------------------------------
# Build the image once (cached afterwards).
# -------------------------------------------------------------------
if ! podman image exists "$IMAGE"; then
  echo ">> Building image $IMAGE..."
  podman build -t "$IMAGE" "$CONTEXT_DIR"
fi

# -------------------------------------------------------------------
# Compile the thesis.
# NOTE: we use --entrypoint sh + explicit cd, because -w (WORKDIR) is
# broken under Git Bash/MSYS on Windows. This form has been validated.
# -------------------------------------------------------------------
echo ">> Compiling thesis..."
podman run --rm \
  -v "${CONTEXT_DIR}:/workdir" \
  --entrypoint sh \
  "$IMAGE" \
  -c "cd /workdir && latexmk -pdf -outdir=build -interaction=nonstopmode main.tex"

echo ">> Done. Output: ${CONTEXT_DIR}/build/main.pdf"
