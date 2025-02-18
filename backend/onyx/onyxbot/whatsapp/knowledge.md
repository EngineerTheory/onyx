# Onyx WhatsApp Bot System

## Overview
WhatsApp bot integration for Onyx, enabling users to interact with Onyx's AI capabilities through WhatsApp. Supports multi-tenant deployments, handles various message types, and provides document integration.

## Key Components

### Message Processing
- Handles user queries and generates AI responses
- Supports chat context and conversation history
- Processes different message types (direct messages, group chats)
- Implements WhatsApp-specific rate limiting and quotas

### Document Integration
- Retrieves and displays relevant documents
- Formats document citations for WhatsApp
- Supports document feedback system
- Handles file attachments and previews

### Security & Authentication
- WhatsApp Business API authentication
- User verification and session management
- Multi-tenant isolation
- Rate limiting and quota management

### User Context Handling
- Users can register their WhatsApp phone number in settings
- Messages from registered numbers are processed in user's context
- Maintains user-specific chat history and preferences
- Enables personalized document access based on user permissions

## Configuration

### Admin Panel Setup
1. Navigate to Admin Panel > Messaging Integrations
2. WhatsApp configuration appears below Slack bot section
3. Configure WhatsApp Business API credentials:
   - Phone Number ID
   - Access Token
   - Webhook Token
4. Enable/disable the WhatsApp bot
5. Configure default chat settings and personas

### User Registration
1. Users must register their WhatsApp number in settings
2. Phone numbers must include country code (e.g. +1234567890)
3. Each phone number can only be registered to one user
4. Users can unregister by clearing their phone number

## Architecture
```
onyxbot/whatsapp/
├── handlers/         # Message and interaction handlers
├── config.py        # WhatsApp configuration
├── formatting.py    # Message formatting utilities
├── listener.py      # Main webhook/message handler
├── models.py        # Data models
└── utils.py         # Helper functions
```

## Technical Constraints
- WhatsApp message format limitations
- API rate limits and quotas
- Message size restrictions
- Authentication requirements
- Webhook handling requirements

## Message Types Support
- Text messages: Primary method for Q&A interactions
- Documents: PDF, DOC, DOCX, etc. with optional captions
- Images: JPG, PNG with optional captions
- Media messages require valid URLs and proper MIME types
- Maximum file size: 16MB for documents, 5MB for images

## Links
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [WhatsApp Rate Limits](https://developers.facebook.com/docs/whatsapp/api/rate-limits)
