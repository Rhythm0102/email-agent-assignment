"""Data models"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Email(BaseModel):
    id: str
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: str
    category: Optional[str] = None
    actions: List[Dict[str, Any]] = []


class PromptConfig(BaseModel):
    categorization_prompt: str
    action_item_prompt: str
    auto_reply_prompt: str


class Draft(BaseModel):
    id: str
    email_id: Optional[str] = None
    subject: str
    body: str
    metadata: Dict[str, Any] = {}
    created_at: str
