"""
Indian Languages & Aksharamukha Transliteration Router.
Provides endpoints for language discovery and script transliteration.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

from jyotishyam.services.transliteration_service import (
    get_supported_languages,
    transliterate_text,
    transliterate_data,
    normalize_script_name
)

router = APIRouter(prefix="/api/v1/languages", tags=["Languages"])


class TransliterateRequest(BaseModel):
    text: Optional[str] = Field(default=None, description="Single text string to transliterate")
    texts: Optional[List[str]] = Field(default=None, description="List of text strings to transliterate")
    payload: Optional[Any] = Field(default=None, description="Arbitrary nested JSON data to transliterate")
    source_script: str = Field(default="Telugu", description="Source script (defaults to Telugu)")
    target_script: str = Field(default="Devanagari", description="Target Indian script")


@router.get("", summary="Get Supported Indian Languages")
def list_languages():
    """Returns list of supported Indian languages and scripts."""
    return {
        "engine": "Aksharamukha Indic Transliteration Engine",
        "default_script": "Telugu",
        "languages": get_supported_languages()
    }


@router.post("/transliterate", summary="Transliterate Content")
def transliterate_endpoint(req: TransliterateRequest):
    """
    Transliterates single text, list of texts, or full nested JSON payload
    from source Indian script (default Telugu) to target Indian script.
    """
    tgt = normalize_script_name(req.target_script)
    src = normalize_script_name(req.source_script)

    resp: Dict[str, Any] = {
        "source_script": src,
        "target_script": tgt
    }

    if req.text is not None:
        resp["text"] = transliterate_text(req.text, tgt, src)

    if req.texts is not None:
        resp["texts"] = [transliterate_text(t, tgt, src) for t in req.texts]

    if req.payload is not None:
        resp["payload"] = transliterate_data(req.payload, tgt, src)

    return resp
