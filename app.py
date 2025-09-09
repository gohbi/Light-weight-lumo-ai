# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# ----------------------------------------------------------------------
# 1️⃣ Import the Model class from pyllamacpp
# ----------------------------------------------------------------------
from pyllamacpp.model import Model  # <-- note the submodule import

from llama_cpp import Llama


# ----------------------------------------------------------------------
# 2️⃣ Create the FastAPI instance
# ----------------------------------------------------------------------
app = FastAPI(
    title="Lumo‑lite inference",
    description="A tiny FastAPI wrapper around a Mistral GGUF model using pyllamacpp.",
    version="0.1.0",
)

# ----------------------------------------------------------------------
# 3️⃣ Load the model – **do NOT pass unsupported kwargs**
# ----------------------------------------------------------------------
# Adjust the path if your model lives elsewhere
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.resolve()
MODEL_PATH = str(BASE_DIR / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf")

try:
    # The current API accepts only the path (plus optional kwargs that are
    # documented in the library – `verbose` and `n_threads` are not among them.
    llm = Model(MODEL_PATH)
except Exception as exc:
    # Fail fast with a clear message – this will surface during import,
    # making the problem obvious.
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {exc}") from exc

# ----------------------------------------------------------------------
# 4️⃣ (Optional) Set the number of threads after construction
# ----------------------------------------------------------------------
# Newer versions expose a setter; if it exists we use it, otherwise we skip.
if hasattr(llm, "set_threads"):
    # Choose a sensible default – you can expose this via an env var later.
    llm.set_threads(4)

# ----------------------------------------------------------------------
# 5️⃣ Request / response schemas
# ----------------------------------------------------------------------
class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 128
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    stop: Optional[List[str]] = None


class CompletionResponse(BaseModel):
    generated_text: str


# ----------------------------------------------------------------------
# 6️⃣ Endpoint implementation
# ----------------------------------------------------------------------
@app.post("/v1/completions", response_model=CompletionResponse)
def generate(req: CompletionRequest):
    """
    Generate a completion using the loaded Mistral GGUF model.
    """
    try:
        # Build the generation parameters dictionary.
        gen_params = {
            "max_tokens": req.max_tokens,
            "temperature": req.temperature,
            "top_p": req.top_p,
        }
        if req.stop:
            gen_params["stop"] = req.stop

        # The Model API returns a list of strings (tokens or chunks).
        # We join them into a single string for the response.
        raw_output = llm.generate(req.prompt, **gen_params)
        # `raw_output` may be a list of strings or a single string.
        if isinstance(raw_output, list):
            generated = "".join(raw_output)
        else:
            generated = str(raw_output)

        return CompletionResponse(generated_text=generated)

    except Exception as e:
        # Surface any generation‑time error as a proper HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))