# Onyx Bot System

## Overview
Core bot system for integrating Onyx with messaging platforms. Currently supports Slack with an extensible architecture for future platforms.

## Architecture
- Platform-specific implementations in subdirectories (e.g. slack/)
- Shared utilities and models at root level
- Event-driven message processing pipeline

## Key Concepts
- Multi-tenant support built-in
- Asynchronous message handling
- Rate limiting and quota management
- Document integration and feedback systems

## Best Practices
- Keep platform-specific code isolated in subdirectories
- Use shared models for cross-platform features
- Implement proper error handling and retries
- Follow rate limiting guidelines for each platform
- Test message formatting across different contexts

## Development Guidelines
- Add new platform integrations in dedicated subdirectories
- Reuse core message processing logic where possible
- Maintain consistent error handling patterns
- Document platform-specific requirements and limitations

## Testing
- Test message processing pipeline
- Verify rate limiting behavior
- Check multi-tenant isolation
- Validate document integration features

## Links
- [Onyx Documentation](https://docs.onyx.org)
- [Slack API Documentation](https://api.slack.com)
