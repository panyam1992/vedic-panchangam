"""
'Talk with Siddhanta Karta / Jyotishya Brahma' Chat Router.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jyotishyam.schemas.chat_models import ChatRequest, ChatResponse
from jyotishyam.services.ai_consultant import consult_siddhanta_karta

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


@router.post("/consult", response_model=ChatResponse)
async def consult_astrologer(req: ChatRequest):
    """
    Ask question to Siddhanta Karta / Jyotishya Brahma.
    The AI uses the user's specific calculated Kundali, Dasha, Gocharam,
    and classical Shastra texts (Uttara Kalamritam, Jataka Chandrika) to answer.
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    history_dicts = [m.model_dump() for m in req.chat_history] if req.chat_history else []
    kundali = req.kundali_data or {}

    result = await consult_siddhanta_karta(
        question=req.question,
        kundali=kundali,
        chat_history=history_dicts,
        language=req.language or "telugu",
        api_key=req.api_key
    )

    return ChatResponse(
        answer=result["answer"],
        shastra_citations=result.get("shastra_citations", []),
        remedies=result.get("remedies", []),
        language=result.get("language", "telugu")
    )


class SetApiKeyRequest(BaseModel):
    api_key: str


@router.post("/set-api-key")
def set_api_key(req: SetApiKeyRequest):
    """Set Gemini API key on server runtime."""
    import os
    os.environ["GEMINI_API_KEY"] = req.api_key.strip()
    return {"status": "success", "message": "Gemini API Key successfully updated."}
