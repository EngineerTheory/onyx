"""
FastAPI application for WhatsApp webhook handling.

This file sets up a basic FastAPI endpoint for WhatsApp webhook verification and incoming message handling.
"""

from fastapi import FastAPI, Request, HTTPException, PlainTextResponse
from onyx.onyxbot.whatsapp import config, utils
from onyx.utils.logger import setup_logger

logger = setup_logger()

app = FastAPI(title="Onyx WhatsApp Bot Listener")

@app.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request) -> str:
    """
    Verification endpoint for WhatsApp webhook.
    WhatsApp sends a GET request to verify the webhook with a challenge.
    """
    params = request.query_params
    verify_token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if not verify_token or not challenge:
        logger.error("Missing verification token or challenge")
        raise HTTPException(status_code=400, detail="Missing required parameters")

    if verify_token != config.WHATSAPP_VERIFY_TOKEN:
        logger.error("Invalid verification token")
        raise HTTPException(status_code=403, detail="Invalid verification token")

    logger.info("Webhook verification successful")
    return challenge

@app.post("/webhook")
async def receive_webhook(request: Request) -> dict[str, str]:
    """
    Endpoint to receive incoming WhatsApp webhook events.
    """
    try:
        payload = await request.json()
        logger.debug(f"Received webhook payload: {payload}")
        await utils.process_incoming_message(payload)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
