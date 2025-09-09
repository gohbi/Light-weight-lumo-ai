# app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyllamacpp.model import Model

# -------------------------------------------------
# Load the GGUF model (once, at startup)
# -------------------------------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral.gguf")
if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found at '{MODEL_PATH}'. "
        "Run 'bash scripts/download_model.sh' to fetch it."
    )

# Initialise the LLM – adjust n_ctx if you need longer context windows
llm = Model(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=os.cpu_count(),
    seed=42,
    verbose=False,
)

# -------------------------------------------------
# FastAPI definition
# -------------------------------------------------
app = FastAPI(
    title="Local‑Lumo (lightweight)",
    version="0.1",
    description="A tiny Lumo‑style chat API using a 4‑bit GGUF model."
)

class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

def _format_prompt(messages: list[ChatMessage]) -> str:
    """
    Convert a list of {role, content} objects into a single prompt
    that the model understands.
    """
    lines = []
    for msg in messages:
        prefix = "User:" if msg.role.lower() == "user" else "Assistant:"
        lines.append(f"{prefix} {msg.content}")
    # Tell the model it should continue as Assistant
    lines.append("Assistant:")
    return "\n".join(lines)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    prompt = _format_prompt(request.messages)

    # Generation parameters – feel free to tweak
    output = llm.generate(
        prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        stop=["User:", "Assistant:"],
    )
    # `output` contains the original prompt; strip it off
    reply = output[len(prompt):].strip()
    return ChatResponse(reply=reply)