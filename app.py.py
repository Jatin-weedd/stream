"""
India Hydro-Vector Data Gateway — Secure Tokenless FGB Proxy
─────────────────────────────────────────────────────────────
"""
import os
import requests
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_url

# ── Config ──────────────────────────────────────────────────────────────────
HF_TOKEN       = os.environ.get("HF_TOKEN")
CLIENT_API_KEY = os.environ.get("CLIENT_API_KEY")

HYDRO_REPO     = "JS2512/hydrology-data-vault"
WATERSHED_FILE = "Watershed.fgb"
STREAMS_FILE   = "Streams.fgb"
REPO_TYPE      = "dataset"

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN environment variable is missing on Render.")

app = FastAPI(
    title="India Hydro-Vector Data Gateway",
    description="Authenticated tokenless router for FlatGeobuf vector layers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

def check_api_key(x_api_key: Optional[str]) -> str:
    if CLIENT_API_KEY and x_api_key != CLIENT_API_KEY:
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key header.")
    return x_api_key or "anonymous"

def _resolve_signed_url(repo_id: str, filename: str, repo_type: str = "dataset") -> str:
    """Uses server-side HF_TOKEN to securely fetch a pre-signed temporary CDN URL."""
    raw_url = hf_hub_url(repo_id=repo_id, filename=filename, repo_type=repo_type)
    resp = requests.head(
        raw_url,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        allow_redirects=True,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.url

# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/resolve/watershed")
def resolve_watershed(x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    url = _resolve_signed_url(HYDRO_REPO, WATERSHED_FILE)
    return {"url": url}

@app.get("/api/v1/resolve/streams")
def resolve_streams(x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    url = _resolve_signed_url(HYDRO_REPO, STREAMS_FILE)
    return {"url": url}