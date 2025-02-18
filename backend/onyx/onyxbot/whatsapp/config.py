from onyx.configs.app_configs import APP_HOST, APP_PORT

# WhatsApp API Configuration
WHATSAPP_API_VERSION = "v15.0"
WHATSAPP_API_BASE_URL = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}"
WHATSAPP_VERIFY_TOKEN = "your_verify_token_here"  # Used for webhook verification
WHATSAPP_ACCESS_TOKEN = "your_access_token_here"  # System User Access Token
WHATSAPP_PHONE_NUMBER_ID = "your_phone_number_id_here"  # Business Phone Number ID

# Webhook Configuration
WEBHOOK_HOST = APP_HOST
WEBHOOK_PORT = APP_PORT
