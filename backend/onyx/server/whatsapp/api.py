"""API endpoints for WhatsApp bot management."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from onyx.db.engine import get_session
from onyx.db.models import WhatsAppBot, WhatsAppChatConfig, User
from onyx.server.auth_check import get_admin_user, get_current_user
from onyx.server.whatsapp.models import (
    WhatsAppBotCreate,
    WhatsAppBotUpdate,
    WhatsAppChatConfigCreate,
    WhatsAppChatConfigUpdate,
    UserWhatsAppUpdate,
)
from onyx.utils.logger import setup_logger

logger = setup_logger()
router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.post("/bots", response_model=dict)
async def create_whatsapp_bot(
    bot_data: WhatsAppBotCreate,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Create a new WhatsApp bot."""
    bot = WhatsAppBot(**bot_data.dict())
    db_session.add(bot)
    try:
        db_session.commit()
        return {"id": bot.id, "status": "success"}
    except Exception as e:
        logger.error(f"Failed to create WhatsApp bot: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create WhatsApp bot")


@router.get("/bots", response_model=List[WhatsAppBot])
async def list_whatsapp_bots(
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> List[WhatsAppBot]:
    """List all WhatsApp bots."""
    return db_session.query(WhatsAppBot).all()


@router.put("/bots/{bot_id}", response_model=dict)
async def update_whatsapp_bot(
    bot_id: int,
    bot_data: WhatsAppBotUpdate,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Update a WhatsApp bot."""
    bot = db_session.query(WhatsAppBot).filter(WhatsAppBot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="WhatsApp bot not found")

    for field, value in bot_data.dict(exclude_unset=True).items():
        setattr(bot, field, value)

    try:
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to update WhatsApp bot: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update WhatsApp bot")


@router.delete("/bots/{bot_id}", response_model=dict)
async def delete_whatsapp_bot(
    bot_id: int,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Delete a WhatsApp bot."""
    bot = db_session.query(WhatsAppBot).filter(WhatsAppBot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="WhatsApp bot not found")

    try:
        db_session.delete(bot)
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to delete WhatsApp bot: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete WhatsApp bot")


# Chat Configuration Endpoints

@router.post("/chat-configs", response_model=dict)
async def create_chat_config(
    config_data: WhatsAppChatConfigCreate,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Create a new WhatsApp chat configuration."""
    config = WhatsAppChatConfig(**config_data.dict())
    db_session.add(config)
    try:
        db_session.commit()
        return {"id": config.id, "status": "success"}
    except Exception as e:
        logger.error(f"Failed to create chat config: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create chat configuration")


@router.get("/chat-configs/{bot_id}", response_model=List[WhatsAppChatConfig])
async def list_chat_configs(
    bot_id: int,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> List[WhatsAppChatConfig]:
    """List all chat configurations for a WhatsApp bot."""
    return db_session.query(WhatsAppChatConfig).filter(
        WhatsAppChatConfig.whatsapp_bot_id == bot_id
    ).all()


@router.put("/chat-configs/{config_id}", response_model=dict)
async def update_chat_config(
    config_id: int,
    config_data: WhatsAppChatConfigUpdate,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Update a WhatsApp chat configuration."""
    config = db_session.query(WhatsAppChatConfig).filter(
        WhatsAppChatConfig.id == config_id
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Chat configuration not found")

    for field, value in config_data.dict(exclude_unset=True).items():
        setattr(config, field, value)

    try:
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to update chat config: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update chat configuration")


@router.delete("/chat-configs/{config_id}", response_model=dict)
async def delete_chat_config(
    config_id: int,
    db_session: Session = Depends(get_session),
    _=Depends(get_admin_user),
) -> dict:
    """Delete a WhatsApp chat configuration."""
    config = db_session.query(WhatsAppChatConfig).filter(
        WhatsAppChatConfig.id == config_id
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Chat configuration not found")

    try:
        db_session.delete(config)
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to delete chat config: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete chat configuration")


@router.put("/user/phone", response_model=dict)
async def update_user_whatsapp_phone(
    phone_data: UserWhatsAppUpdate,
    db_session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> dict:
    """Update the current user's WhatsApp phone number."""
    try:
        # If phone number is being cleared, just set to None
        if phone_data.whatsapp_phone_number is None:
            current_user.whatsapp_phone_number = None
        else:
            # Check if phone number is already registered to another user
            existing_user = (
                db_session.query(User)
                .filter(
                    User.whatsapp_phone_number == phone_data.whatsapp_phone_number,
                    User.id != current_user.id,
                )
                .first()
            )
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="This WhatsApp number is already registered to another user",
                )
            current_user.whatsapp_phone_number = phone_data.whatsapp_phone_number

        db_session.add(current_user)
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to update WhatsApp phone number: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update WhatsApp phone number",
        )
