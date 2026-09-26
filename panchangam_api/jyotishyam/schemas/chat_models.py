"""
Chat models for 'Talk with Siddhanta Karta / Jyotishya Brahma'.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message text")


class ChatRequest(BaseModel):
    question: str = Field(..., description="User's life question to the astrologer")
    kundali_data: Optional[Dict[str, Any]] = Field(None, description="Full calculated Kundali payload")
    chat_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation history")
    language: Optional[str] = Field(default="telugu", description="'telugu' or 'english'")
    api_key: Optional[str] = Field(default=None, description="Optional Gemini API key from user or frontend")


class ChatResponse(BaseModel):
    answer: str
    shastra_citations: List[str]
    remedies: List[str]
    language: str
