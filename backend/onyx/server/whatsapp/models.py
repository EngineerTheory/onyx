"""Models for WhatsApp bot management API."""

from typing import Optional
from pydantic import BaseModel, constr


class WhatsAppBotCreate(BaseModel):
    """Model for creating a new WhatsApp bot."""
    name: str
    phone_number_id: str
    access_token: str
    webhook_token: str
    enabled: bool = True


class WhatsAppBotUpdate(BaseModel):
    """Model for updating a WhatsApp bot."""
    name: Optional[str] = None
    phone_number_id: Optional[str] = None
    access_token: Optional[str] = None
    webhook_token: Optional[str] = None
    enabled: Optional[bool] = None


class WhatsAppChatConfigCreate(BaseModel):
    """Model for creating a new WhatsApp chat configuration."""
    whatsapp_bot_id: int
    chat_id: str
    chat_name: Optional[str] = None
    chat_type: str
    persona_id: Optional[int] = None
    enable_auto_filters: bool = False
    is_default: bool = False


class WhatsAppChatConfigUpdate(BaseModel):
    """Model for updating a WhatsApp chat configuration."""
    chat_name: Optional[str] = None
    persona_id: Optional[int] = None
    enable_auto_filters: Optional[bool] = None
    is_default: Optional[bool] = None


class UserWhatsAppUpdate(BaseModel):
    """Model for updating a user's WhatsApp phone number."""
    whatsapp_phone_number: Optional[constr(regex=r'^\+[1-9]\d{1,14}$')] = None
