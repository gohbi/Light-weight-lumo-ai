#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Download a 4‑bit GGUF checkpoint for Mistral‑7B‑Instruct.
# This file is ~1.2 GB. Adjust the URL if you prefer a different model.
# ------------------------------------------------------------------

MODEL_DIR="$(dirname "$(realpath "$0")")/../models"
mkdir -p "$MODEL_DIR"

# Target filename
TARGET="${MODEL_DIR}/mistral.gguf"

# If the file already exists, skip download
if [[ -f "$TARGET" ]]; then
    echo "Model already present at $TARGET"
    exit 0
fi

# URL of the quantised GGUF model (publicly hosted on HuggingFace)
URL="https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

echo "Downloading Mistral‑7B‑Instruct (4‑bit GGUF)…"
# Use curl with progress bar; fallback to wget if curl missing
if command -v curl >/dev/null; then
    curl -L -o "$TARGET" "$URL"
elif command -v wget >/dev/null; then
    wget -O "$TARGET" "$URL"
else
    echo "Neither curl nor wget is installed. Install one and retry."
    exit 1
fi

echo "✅ Model saved to $TARGET"