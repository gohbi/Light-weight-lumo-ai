# Local‑Lumo (lightweight)

A tiny, privacy‑first chat API that mimics Lumo, built to run inside a GitHub Codespace or any environment with limited disk space.

## Features
- **No PyTorch / Transformers** – uses `pyllamacpp` + a 4‑bit GGUF model (~1 GB).
- FastAPI + Uvicorn HTTP server.
- Simple prompt format (`User:` / `Assistant:`).
- One‑click model downloader (`scripts/download_model.sh`).

## Quick start (inside a Codespace)

```bash
# 1️⃣ Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Download the quantised model (≈1 GB)
bash scripts/download_model.sh

# 4️⃣ Run the API
uvicorn app:app --host 0.0.0.0 --port 8000
