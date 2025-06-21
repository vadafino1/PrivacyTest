# PrivacyTest - Vulnerability Testing Repository

⚠️ **WARNING: This repository contains intentionally vulnerable code for testing privacy scanning tools. DO NOT USE IN PRODUCTION.**

## Overview

This repository contains 150+ documented privacy and security vulnerabilities designed to test privacy scanning tools and security analysis software. It includes realistic patterns of PII exposure, hardcoded secrets, weak authentication, and compliance violations.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/vadafino1/PrivacyTest.git
cd PrivacyTest

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Start vulnerable applications
npm start           # Node.js server on port 3000
python app.py       # Python Flask app on port 5000

# Or use Docker
docker-compose up
```

## Repository Contents

### Applications
- **server.js** - Node.js/Express server with API vulnerabilities
- **app.py** - Python/Flask application with authentication flaws
- **config.json** - Configuration with exposed secrets
- **.env** - Environment variables with production credentials

### Data Files
- **users.csv** - User database with PII (SSNs, credit cards, medical data)
- **employee_data.json** - Employee records with sensitive information
- **backup.sql** - Database dump with complete user data
- **payment_logs.txt** - Transaction logs with payment details

### Log Files
- **application.log** - Debug logs with credentials and PII
- **access.log** - HTTP logs with tracking data and tokens
- **error.log** - Error logs with stack traces and secrets
- **audit.log** - Admin activity logs with violations

## Vulnerability Categories

- **Privacy/PII Exposure** (45+ issues) - SSNs, credit cards, medical data
- **Hardcoded Secrets** (35+ issues) - API keys, passwords, tokens
- **Authentication Issues** (20+ issues) - Weak auth, missing controls
- **Data Exposure** (25+ issues) - Debug endpoints, error leaks
- **Logging Violations** (30+ issues) - Sensitive data in logs

## Testing Your Tools

This repository is designed to test:
- PII detection (SSN, credit card, medical patterns)
- Secret scanning (API keys, passwords, tokens)
- Compliance violations (GDPR, HIPAA, PCI DSS)
- Access control weaknesses
- Data retention failures

## Documentation

- **VULNERABILITY_RECORD.md** - Complete list of all 150+ vulnerabilities
- **CLAUDE.md** - Development guidance for this repository

## Legal Notice

This repository is for educational and defensive security testing only. All data is synthetic. Do not use these patterns in production systems.