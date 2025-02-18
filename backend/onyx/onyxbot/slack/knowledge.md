# Onyx Slack Bot

## Overview
The Slack bot integration enables users to interact with Onyx's AI capabilities directly through Slack. The bot supports multi-tenant deployments, handles various message types, and provides interactive features like feedback and follow-ups.

## Key Components

### Message Processing
- Handles user queries and generates AI responses
- Supports thread context and conversation history
- Processes different message types (direct messages, mentions)

### Document Integration
- Retrieves and displays relevant documents
- Formats document citations and references
- Supports document feedback system

### Interactive Features
- Feedback buttons for answer quality
- Follow-up request handling
- Document relevance feedback

## Configuration
- Each tenant can have multiple Slack bots
- Channel-specific configurations available
- Rate limiting and quota management

## Best Practices
- Use thread replies for long conversations
- Implement proper error handling and retries
- Follow Slack's rate limiting guidelines
- Test message formatting in different contexts

## Architecture
```
onyxbot/slack/
├── handlers/         # Message and interaction handlers
├── blocks.py        # Slack Block Kit UI components
├── config.py        # Bot configuration
├── formatting.py    # Message formatting utilities
├── listener.py      # Main WebSocket handler
├── models.py        # Data models
└── utils.py         # Helper functions
```

## Links
- [Slack Block Kit Documentation](https://api.slack.com/block-kit)
- [Slack Socket Mode API](https://api.slack.com/apis/connections/socket)
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits)
