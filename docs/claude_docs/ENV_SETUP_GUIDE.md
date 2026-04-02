# Environment Setup Guide

## Quick Start

1. **Copy the example file**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**
   ```bash
   # Windows
   notepad .env
   
   # Linux/Mac
   nano .env
   ```

3. **Fill in required values** (see sections below)

---

## Required Configuration

### 1. Database Connection ⚠️ REQUIRED

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/regulatory_reporting
```

**Setup PostgreSQL:**
```bash
# Create database
psql -U postgres
CREATE DATABASE regulatory_reporting;
\q
```

### 2. Security Settings ⚠️ REQUIRED FOR PRODUCTION

```bash
# CHANGE THIS IN PRODUCTION!
SECRET_KEY=your-super-secret-key-minimum-32-characters-long
```

**Generate secure key:**
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### 3. LLM Provider ⚠️ REQUIRED FOR AI FEATURES

Choose **one** of the following:

#### Option A: Azure OpenAI (Recommended)

```bash
# Provider
LLM_PROVIDER=azure

# Azure OpenAI Credentials
AZURE_OPENAI_ENDPOINT=https://agent-alm.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Model Configuration
DEFAULT_MODEL_NAME=gpt-4.1
LLM_MODEL_NAME=gpt-4.1
DEFAULT_TEMPERATURE=0.1
LLM_TEMPERATURE=0.1
DEFAULT_MAX_TOKENS=4096
LLM_MAX_TOKENS=4096
DEFAULT_TOP_P=1.0
LLM_TOP_P=1.0
```

#### Option B: OpenAI

```bash
# Provider
LLM_PROVIDER=openai

# OpenAI Credentials
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Model Configuration
DEFAULT_MODEL_NAME=gpt-4-turbo-preview
LLM_MODEL_NAME=gpt-4-turbo-preview
DEFAULT_TEMPERATURE=0.1
LLM_TEMPERATURE=0.1
DEFAULT_MAX_TOKENS=4096
LLM_MAX_TOKENS=4096
DEFAULT_TOP_P=1.0
LLM_TOP_P=1.0
```

---

## Complete .env Template

### For Azure OpenAI (Recommended)

```bash
# Application Settings
ENVIRONMENT=development
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/regulatory_reporting

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Provider Configuration
LLM_PROVIDER=azure

# OpenAI API (not needed for Azure)
OPENAI_API_KEY=

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://agent-alm.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Model Configuration
DEFAULT_MODEL_NAME=gpt-4.1
LLM_MODEL_NAME=gpt-4.1
DEFAULT_TEMPERATURE=0.1
LLM_TEMPERATURE=0.1
DEFAULT_MAX_TOKENS=4096
LLM_MAX_TOKENS=4096
DEFAULT_TOP_P=1.0
LLM_TOP_P=1.0

# Storage - All application files stored in this folder
STORAGE_PATH=./storage

# ChromaDB - Vector database stored inside storage folder
CHROMA_PATH=./storage/chroma_data

# Rate Limiting
RATE_LIMIT_ENABLED=True
MAX_REQUESTS_PER_MINUTE=60

# Cleanup Settings
CLEANUP_INTERVAL_HOURS=24
SESSION_EXPIRY_DAYS=7
CACHE_EXPIRY_HOURS=1
RATE_LIMIT_EXPIRY_HOURS=1
TEMP_FILE_EXPIRY_DAYS=1

# Agent Settings
AGENT_TIMEOUT_SECONDS=300
MAX_AGENT_RETRIES=3

# Logging
LOG_LEVEL=INFO
```

---

## Configuration Checklist

### Development Environment

- [x] Copy `.env.example` to `.env`
- [ ] Set `DATABASE_URL` (PostgreSQL connection)
- [ ] Set `SECRET_KEY` (any random string for dev)
- [ ] Set `LLM_PROVIDER` (`azure` or `openai`)
- [ ] Set Azure OpenAI credentials OR OpenAI API key
- [ ] Set model configuration parameters
- [ ] Create PostgreSQL database
- [ ] Run `python app.py` to verify

### Production Environment

- [x] Copy `.env.example` to `.env`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Set `DATABASE_URL` (production database)
- [ ] **Generate secure `SECRET_KEY`** ⚠️
- [ ] Set `LLM_PROVIDER`
- [ ] Set Azure OpenAI credentials (recommended)
- [ ] Configure rate limiting (review limits)
- [ ] Configure cleanup intervals
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Enable SSL/TLS
- [ ] Set up firewall rules
- [ ] Configure backup strategy
- [ ] Set up monitoring

---

## Getting Azure OpenAI Credentials

### Step 1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Azure OpenAI"
4. Click "Create"
5. Fill in:
   - Resource group: Create new or select existing
   - Region: Choose closest region
   - Name: `your-company-openai`
   - Pricing tier: Select appropriate tier

### Step 2: Deploy a Model

1. Go to your Azure OpenAI resource
2. Click "Model deployments" → "Manage Deployments"
3. Click "Create new deployment"
4. Select:
   - Model: `gpt-4` or `gpt-4-turbo`
   - Deployment name: `gpt-4.1` (use this in AZURE_OPENAI_DEPLOYMENT)
   - Model version: Latest stable
5. Click "Create"

### Step 3: Get Credentials

1. Go to your Azure OpenAI resource
2. Click "Keys and Endpoint"
3. Copy:
   - **Endpoint**: Use for `AZURE_OPENAI_ENDPOINT`
   - **Key 1**: Use for `AZURE_OPENAI_API_KEY`

### Step 4: Update .env

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=abc123...your-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
```

---

## Getting OpenAI API Key

### Step 1: Create OpenAI Account

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Add payment method

### Step 2: Create API Key

1. Click on your profile → "API keys"
2. Click "Create new secret key"
3. Name it: "NTT Data Regulatory System"
4. Copy the key (you can only see it once!)

### Step 3: Update .env

```bash
OPENAI_API_KEY=sk-...your-key-here
```

---

## Verification

### 1. Test Database Connection

```bash
cd backend
python -c "
import asyncio
from app.db.postgres import check_db_connection

async def test():
    result = await check_db_connection()
    print('Database:', result)

asyncio.run(test())
"
```

### 2. Test LLM Connection

```bash
python -c "
from app.core.llm_client import get_llm_client

client = get_llm_client()
info = client.get_model_info()
print('Provider:', info['provider'])
print('Model:', info['model_name'])

# Test completion
response = client.chat_completion([
    {'role': 'user', 'content': 'Say hello'}
])
print('Response:', client.extract_response_text(response))
"
```

### 3. Test Application Startup

```bash
python app.py
```

Should see:
```
📁 Setting up storage directories...
✅ Created 54 storage directories under storage
🗄️  Initializing database...
✅ Database initialized successfully
...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# API docs
open http://localhost:8000/api/v1/docs
```

---

## Common Issues

### Issue: "Database connection failed"

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   # Windows
   net start postgresql-x64-14
   
   # Linux
   sudo systemctl status postgresql
   
   # Mac
   brew services list | grep postgresql
   ```

2. Verify database exists:
   ```bash
   psql -U postgres -c "\l" | grep regulatory_reporting
   ```

3. Check credentials in DATABASE_URL

### Issue: "AZURE_OPENAI_API_KEY is required"

**Solutions:**
1. Ensure LLM_PROVIDER=azure in .env
2. Check AZURE_OPENAI_API_KEY is set
3. Verify no extra spaces in API key

### Issue: "Invalid endpoint"

**Solutions:**
1. Check endpoint format:
   ```bash
   # Correct
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   
   # Incorrect (remove /openai/...)
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/deployments/...
   ```

### Issue: "Deployment not found"

**Solutions:**
1. Check deployment name matches Azure portal exactly
2. Verify deployment is in "Succeeded" state
3. Wait a few minutes if just created

---

## Environment-Specific Configurations

### Local Development

```bash
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=False  # Easier testing
```

### Staging

```bash
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
MAX_REQUESTS_PER_MINUTE=100
```

### Production

```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
RATE_LIMIT_ENABLED=True
MAX_REQUESTS_PER_MINUTE=60
SESSION_EXPIRY_DAYS=1  # More secure
CLEANUP_INTERVAL_HOURS=6  # More frequent
```

---

## Security Best Practices

### 1. Never Commit .env Files

```bash
# Already in .gitignore
cat .gitignore | grep .env
```

### 2. Use Different Keys Per Environment

- **Development**: Test keys
- **Staging**: Staging keys
- **Production**: Production keys (rotate regularly)

### 3. Restrict Database Access

```sql
-- Create read-only user for reporting
CREATE USER reporting_readonly WITH PASSWORD 'secure-password';
GRANT CONNECT ON DATABASE regulatory_reporting TO reporting_readonly;
GRANT USAGE ON SCHEMA public TO reporting_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_readonly;
```

### 4. Monitor API Usage

- Set up billing alerts in Azure/OpenAI
- Monitor token usage
- Implement rate limiting

---

## Related Documentation

- [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) - Detailed LLM setup
- [STORAGE_STRUCTURE.md](STORAGE_STRUCTURE.md) - Storage configuration
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) - System validation
- [README.md](README.md) - Main documentation

---

**Last Updated**: 2026-04-02  
**Version**: 1.0.0
