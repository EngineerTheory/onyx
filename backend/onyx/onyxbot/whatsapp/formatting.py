"""
WhatsApp message formatting utilities.

These functions convert messages into formats acceptable for the WhatsApp API.
"""

from typing import Any, Optional

from onyx.utils.logger import setup_logger

logger = setup_logger()


def format_text_message(text: str, recipient: str) -> dict[str, Any]:
    """Format a plain text message for WhatsApp API.

    Args:
        text: The message text to send
        recipient: The recipient's phone number

    Returns:
        A dictionary formatted for the WhatsApp API
    """
    return {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": text},
    }


def format_document_message(
    document_url: str, recipient: str, caption: Optional[str] = None
) -> dict[str, Any]:
    """Format a document message for WhatsApp API.

    Args:
        document_url: URL of the document to send
        recipient: The recipient's phone number
        caption: Optional caption for the document

    Returns:
        A dictionary formatted for the WhatsApp API
    """
    return {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "document",
        "document": {
            "link": document_url,
            "caption": caption or "",
        },
    }


def format_image_message(
    image_url: str, recipient: str, caption: Optional[str] = None
) -> dict[str, Any]:
    """Format an image message for WhatsApp API.

    Args:
        image_url: URL of the image to send
        recipient: The recipient's phone number
        caption: Optional caption for the image

    Returns:
        A dictionary formatted for the WhatsApp API
    """
    return {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption or "",
        },
    }
