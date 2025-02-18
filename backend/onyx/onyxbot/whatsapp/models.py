"""
Data models for WhatsApp integration.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WhatsAppMessage(BaseModel):
    """Represents an incoming WhatsApp message."""

    from_number: str
    to_number: Optional[str] = None
    message_body: str
    timestamp: datetime
    message_type: str = "text"
    media_url: Optional[str] = None


class WhatsAppResponse(BaseModel):
    """Represents an outgoing WhatsApp message."""

    messaging_product: str = "whatsapp"
    to: str
    type: str
    text: Optional[dict[str, str]] = None
    document: Optional[dict[str, str]] = None
