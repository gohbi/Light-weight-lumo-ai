# app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyllamacpp.model import Model

# -------------------------------------------------
# Load the GGUF model (once, at startup)
# -------------------------------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral.gguf")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

# `n_ctx` = context length, adjust if you need longer windows
llm = Model(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=os.cpu_count(),          # use all CPU cores
    seed=42,
    verbose=False,
)

# -------------------------------------------------
# FastAPI definition
# -------------------------------------------------
app = FastAPI(title="Local‑Lumo (gguf)", version="0.1")

class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

def _format_prompt(messages: list[ChatMessage]) -> str:
    """
    Turn a list of {role, content} dicts into a single prompt.
    Simple format: "User: ...\nAssistant: ..."
    """
    lines = []
    for msg in messages:
        prefix = "User:" if msg.role.lower() == "user" else "Assistant:"
        lines.append(f"{prefix} {msg.content}")
    # Ensure the model knows it should continue as Assistant
    lines.append("Assistant:")
    return "\n".join(lines)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    prompt = _format_prompt(req.messages)

    # Generation parameters – tweak as you like
    output = llm.generate(
        prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        stop=["User:", "Assistant:"],
    )
    # `output` includes the original prompt; strip it
    reply = output[len(prompt):].strip()
    return ChatResponse(reply=reply)