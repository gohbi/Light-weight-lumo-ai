# Lightweight Lumo AI

A lightweight, privacy-first AI chat API inspired by Proton's Lumo. This project provides a minimal, locally-runnable alternative that you can integrate into your own applications without the overhead of large ML frameworks.

**Perfect for:**
- Running AI chat locally on your machine
- Integrating AI capabilities into personal projects
- Learning how to build AI-powered APIs
- Privacy-conscious applications that keep data local
- GitHub Codespaces or environments with limited disk space

## What is Lumo?

Lumo is an AI chat assistant feature from Proton. This project creates a lightweight version that:
- Runs completely locally (no external API calls)
- Uses minimal resources (~1 GB model)
- Provides a simple REST API for easy integration
- Maintains privacy by keeping all data on your machine

## Features

- **Lightweight** - No PyTorch or Transformers library required
- **Small footprint** - Uses `pyllamacpp` with a 4-bit quantized GGUF model (~1 GB)
- **Fast API** - Built with FastAPI + Uvicorn for high-performance HTTP serving
- **Privacy-first** - Everything runs locally, no data sent to external services
- **Easy setup** - One-click model downloader included
- **Flexible** - Simple REST API that can be integrated into any project

## Quick Start

### Prerequisites
- Python 3.8 or higher
- ~1.5 GB free disk space for the model

### Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/gohbi/Light-weight-lumo-ai.git
cd Light-weight-lumo-ai

# 2️⃣ Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Download the quantized model (~1 GB)
bash scripts/download_model.sh

# 5️⃣ Run the API server
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Using in GitHub Codespaces

This project is optimized for GitHub Codespaces with a pre-configured development container:

1. Open the repository in GitHub Codespaces
2. The devcontainer will automatically set up the environment
3. Once setup completes, run: `uvicorn app:app --host 0.0.0.0 --port 8000`

## API Usage

### Generate Completions

Send a POST request to `/v1/completions` with your prompt:

```bash
curl -X POST "http://localhost:8000/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "User: What is the capital of France?\nAssistant:",
    "max_tokens": 128,
    "temperature": 0.7,
    "top_p": 0.9
  }'
```

**Request Parameters:**
- `prompt` (required): The input text prompt
- `max_tokens` (optional, default: 128): Maximum number of tokens to generate
- `temperature` (optional, default: 0.7): Controls randomness (0.0-1.0)
- `top_p` (optional, default: 0.9): Nucleus sampling parameter
- `stop` (optional): List of strings where generation should stop

**Response:**
```json
{
  "generated_text": "The capital of France is Paris."
}
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Project Structure

```
Light-weight-lumo-ai/
├── app.py                  # Main FastAPI application
├── requirements.txt        # Python dependencies
├── scripts/
│   └── download_model.sh   # Model download script
├── models/                 # Downloaded models stored here
├── .devcontainer/          # GitHub Codespaces configuration
└── README.md              # This file
```

## Using in Your Projects

You can integrate this API into your projects in several ways:

### 1. As a Local Microservice

Run the API locally and call it from your application:

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/completions",
    json={
        "prompt": "User: Hello!\nAssistant:",
        "max_tokens": 100
    }
)
print(response.json()["generated_text"])
```

### 2. Import the Model Directly

You can also import and use the model directly in your Python code:

```python
from pyllamacpp.model import Model

model = Model("models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
response = model.generate("User: Hello!\nAssistant:", max_tokens=100)
print(response)
```

### 3. Customize the API

Fork this repository and modify `app.py` to add custom endpoints, preprocessing, or features specific to your needs.

## Model Information

This project uses the Mistral-7B-Instruct-v0.2 model in GGUF format with Q4_K_M quantization:
- **Model**: Mistral-7B-Instruct-v0.2
- **Format**: GGUF (GPT-Generated Unified Format)
- **Quantization**: Q4_K_M (4-bit quantization with K-means)
- **Size**: ~1 GB
- **Source**: TheBloke's quantized models on HuggingFace

## Configuration

You can customize the model path and other settings by editing `app.py`:

```python
# Change the model path
MODEL_PATH = str(BASE_DIR / "models" / "your-model-name.gguf")

# Adjust thread count (if supported)
if hasattr(llm, "set_threads"):
    llm.set_threads(8)  # Use 8 threads
```

## Troubleshooting

### Model download fails
- Ensure you have a stable internet connection
- Check that you have ~1.5 GB free disk space
- Try downloading manually from the URL in `scripts/download_model.sh`

### Out of memory errors
- The model requires at least 2 GB of RAM
- Close other applications to free up memory
- Consider using a smaller quantized model (Q2 or Q3)

### Import errors
- Ensure you've activated the virtual environment
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Proton's Lumo AI assistant
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [pyllamacpp](https://github.com/abdeladim-s/pyllamacpp) for model inference
- Model by [Mistral AI](https://mistral.ai/)
- Quantized by [TheBloke](https://huggingface.co/TheBloke)

## Disclaimer

This is an independent project and is not affiliated with or endorsed by Proton AG. Lumo is a trademark of Proton AG.
