# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **vulnerability testing repository** containing intentionally insecure code and data for testing privacy scanning tools. It contains 150+ documented privacy and security vulnerabilities across multiple categories including PII exposure, hardcoded secrets, weak authentication, and logging violations.

**⚠️ CRITICAL: This repository contains intentionally vulnerable code designed for defensive security testing only. Never use any code, configuration, or patterns from this repository in production environments.**

## Architecture Overview

The repository simulates a multi-component application with privacy vulnerabilities:

### Core Components
- **app.py**: Python/Flask application with embedded credentials, SQL injection, weak authentication, and PII logging
- **server.js**: Node.js/Express server with similar vulnerability patterns, insecure session management, and debug endpoints
- **config.json**: Configuration file with exposed API keys, database credentials, and third-party service tokens
- **.env**: Environment variables containing production secrets, AWS credentials, and service keys

### Data Files (Containing Synthetic PII)
- **users.csv**: User database with SSNs, credit cards, medical conditions, and weak passwords
- **employee_data.json**: Employee records with banking details, health information, and background checks
- **backup.sql**: Database dump with complete user data, payment methods, and medical records
- **payment_logs.txt**: Transaction logs with full credit card details and customer information

### Log Files (Privacy Violations)
- **application.log**: Debug logs containing credentials, user passwords, PII in stack traces, and API keys
- **access.log**: HTTP access logs with user emails, SSNs in URLs, authentication tokens, and tracking data
- **error.log**: Error logs with database credentials, environment variables, and system information
- **audit.log**: Admin activity logs showing data access violations and compliance breaches

### Infrastructure
- **docker-compose.yml**: Container configuration with exposed database passwords and insecure defaults
- **Dockerfile**: Container setup running as root with hardcoded secrets and vulnerable configurations

## Common Commands

### Application Execution
```bash
# Start Node.js server (port 3000)
npm start

# Start in development mode with nodemon
npm run dev

# Run Python Flask app
python app.py

# Start all services with Docker Compose
docker-compose up
```

### Docker Operations
```bash
# Build container image
npm run docker:build

# Run containerized application
npm run docker:run

# Full stack with databases
docker-compose up -d
```

### Testing and Analysis
```bash
# Run test suite (if implementing tests)
npm test

# Build production bundle
npm run build
```

## Vulnerability Categories

When working with this codebase, be aware of these intentional vulnerability patterns:

1. **Hardcoded Secrets**: API keys, database passwords, and tokens embedded in source code
2. **PII Exposure**: SSNs, credit cards, medical data in logs, responses, and data files
3. **Authentication Bypasses**: Weak password policies, hardcoded credentials, missing authorization
4. **Data Leakage**: Debug endpoints, error messages, and logs exposing sensitive information
5. **Infrastructure Issues**: Insecure container configurations, exposed services, weak encryption

## Development Guidelines

### Adding New Vulnerabilities
- Follow existing patterns for consistency with privacy scanning tool expectations
- Document new vulnerabilities in VULNERABILITY_RECORD.md with specific line numbers
- Ensure secrets don't trigger GitHub's push protection (use modified patterns like "TWL" instead of "AC" for Twilio)
- Include synthetic but realistic PII data that scanning tools can detect

### File Patterns
- **Source code**: Embed credentials, use weak crypto, log sensitive data
- **Configuration**: Plaintext secrets, insecure settings, exposed endpoints
- **Data files**: Realistic PII patterns (SSNs, credit cards, medical data)
- **Logs**: Stack traces with secrets, user activity with PII, audit trails with violations

### Testing Integration
When adding privacy scanning tools, ensure they can detect:
- Embedded credentials in source code and configuration
- PII patterns in data files and logs
- Weak authentication and authorization mechanisms
- Compliance violations (GDPR, HIPAA, PCI DSS)
- Third-party data sharing without consent

This repository serves as a comprehensive test case for privacy and security scanning tools, representing common real-world vulnerability patterns in a controlled environment.