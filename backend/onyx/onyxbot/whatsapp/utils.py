"""
Helper functions for WhatsApp integration.
"""

from typing import Any, Optional
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from onyx.onyxbot.whatsapp.config import (
    WHATSAPP_API_BASE_URL,
    WHATSAPP_ACCESS_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
)
from onyx.utils.logger import setup_logger
from onyx.db.models import WhatsAppBot, WhatsAppChatConfig, User
from onyx.chat.process_message import process_message
from onyx.onyxbot.whatsapp.formatting import (
    format_text_message,
    format_document_message,
    format_image_message
)

logger = setup_logger()


async def get_whatsapp_bot(db_session: Session, bot_id: int) -> WhatsAppBot:
    """Get WhatsApp bot configuration from database.

    Args:
        db_session: Database session
        bot_id: ID of the WhatsApp bot

    Returns:
        WhatsApp bot configuration

    Raises:
        HTTPException: If bot not found
    """
    bot = db_session.query(WhatsAppBot).filter(WhatsAppBot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="WhatsApp bot not found")
    return bot


async def get_chat_config(
    db_session: Session, bot_id: int, chat_id: str
) -> WhatsAppChatConfig:
    """Get chat configuration for a specific chat.

    Args:
        db_session: Database session
        bot_id: ID of the WhatsApp bot
        chat_id: Chat identifier

    Returns:
        Chat configuration

    Raises:
        HTTPException: If chat config not found
    """
    chat_config = (
        db_session.query(WhatsAppChatConfig)
        .filter(
            WhatsAppChatConfig.whatsapp_bot_id == bot_id,
            WhatsAppChatConfig.chat_id == chat_id,
        )
        .first()
    )
    if not chat_config:
        # Try to get default config
        chat_config = (
            db_session.query(WhatsAppChatConfig)
            .filter(
                WhatsAppChatConfig.whatsapp_bot_id == bot_id,
                WhatsAppChatConfig.is_default.is_(True),
            )
            .first()
        )
    if not chat_config:
        raise HTTPException(status_code=404, detail="Chat configuration not found")
    return chat_config


async def get_user_by_phone(
    db_session: Session, phone_number: str
) -> Optional[User]:
    """Get user by their registered WhatsApp phone number.

    Args:
        db_session: Database session
        phone_number: WhatsApp phone number

    Returns:
        User if found, None otherwise
    """
    return (
        db_session.query(User)
        .filter(User.whatsapp_phone_number == phone_number)
        .first()
    )


async def send_whatsapp_message(payload: dict[str, Any]) -> dict[str, Any]:
    """Send a message via WhatsApp API.

    Args:
        payload: The message payload to send

    Returns:
        The API response

    Raises:
        HTTPException: If the API request fails
    """
    url = f"{WHATSAPP_API_BASE_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"WhatsApp API request failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to send WhatsApp message: {str(e)}"
        )


async def process_incoming_message(
    db_session: Session, bot_id: int, payload: dict[str, Any]
) -> None:
    """Process an incoming WhatsApp webhook payload.

    Args:
        db_session: Database session
        bot_id: ID of the WhatsApp bot
        payload: The webhook payload from WhatsApp

    Raises:
        HTTPException: If processing fails
    """
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    messages = change.get("value", {}).get("messages", [])
                    for msg in messages:
                        await handle_message(db_session, bot_id, msg)
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook payload: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process webhook payload: {str(e)}"
        )


async def handle_message(
    db_session: Session, bot_id: int, message: dict[str, Any]
) -> None:
    """Handle a single WhatsApp message.

    Args:
        db_session: Database session
        bot_id: ID of the WhatsApp bot
        message: The message data from WhatsApp
    """
    try:
        from_number = message.get("from")
        message_type = message.get("type")
        chat_id = from_number  # For individual chats, chat_id is the phone number

        # Check if user is registered etc.
        user = await get_user_by_phone(db_session, from_number)
        chat_config = await get_chat_config(db_session, bot_id, chat_id)
        
        if message_type == "text":
            text = message.get("text", {}).get("body")
            logger.info(f"Received text message from {from_number}: {text}")
            response = await process_message(
                db_session=db_session,
                message=text,
                chat_id=chat_id,
                persona_id=chat_config.persona_id,
                user=user,
            )
            await send_whatsapp_message(format_text_message(response.message, from_number))
        
        elif message_type in ["document", "image"]:
            media = message.get(message_type, {})
            logger.info(f"Received {message_type} from {from_number}")
            if message_type == "document":
                document_url = media.get("link", "")
                caption = media.get("caption", "")
                payload = format_document_message(document_url, from_number, caption)
            elif message_type == "image":
                image_url = media.get("link", "")
                caption = media.get("caption", "")
                payload = format_image_message(image_url, from_number, caption)
            await send_whatsapp_message(payload)
        
        else:
            logger.warning(f"Unsupported message type: {message_type}")
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
