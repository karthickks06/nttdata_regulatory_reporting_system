# LLM Configuration Guide

## Overview

The NTT Data Regulatory Reporting System supports both **OpenAI** and **Azure OpenAI** as LLM providers. This guide explains how to configure and use each provider.

---

## Supported Providers

### 1. Azure OpenAI (Recommended for Enterprise)
- ✅ Enterprise-grade security
- ✅ Regional data residency
- ✅ SLA guarantees
- ✅ VNet integration
- ✅ Private endpoints

### 2. OpenAI (Public API)
- ✅ Latest models first
- ✅ Simple setup
- ✅ Pay-as-you-go pricing

---

## Configuration

### Environment Variables

All LLM configuration is done via environment variables in the `.env` file.

#### Azure OpenAI Configuration

```bash
# LLM Provider
LLM_PROVIDER=azure

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
```

#### OpenAI Configuration

```bash
# LLM Provider
LLM_PROVIDER=openai

# OpenAI API
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

## Configuration Parameters

### Core Settings

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `LLM_PROVIDER` | Provider to use | `azure` | `azure` or `openai` |

### Azure OpenAI Settings

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes | `abc123...` |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name | Yes | `gpt-4.1` |
| `AZURE_OPENAI_API_VERSION` | API version | Yes | `2024-12-01-preview` |

### OpenAI Settings

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | `sk-...` |

### Model Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `DEFAULT_MODEL_NAME` | Default model name | `gpt-4.1` | Any valid model |
| `LLM_MODEL_NAME` | LLM model name | `gpt-4.1` | Any valid model |
| `DEFAULT_TEMPERATURE` | Sampling temperature | `0.1` | 0.0 - 2.0 |
| `LLM_TEMPERATURE` | LLM temperature | `0.1` | 0.0 - 2.0 |
| `DEFAULT_MAX_TOKENS` | Max tokens to generate | `4096` | 1 - 32768 |
| `LLM_MAX_TOKENS` | LLM max tokens | `4096` | 1 - 32768 |
| `DEFAULT_TOP_P` | Nucleus sampling | `1.0` | 0.0 - 1.0 |
| `LLM_TOP_P` | LLM top_p | `1.0` | 0.0 - 1.0 |

---

## Usage

### Basic Usage

```python
from app.core.llm_client import get_llm_client

# Get client instance
client = get_llm_client()

# Simple chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is regulatory reporting?"}
]

response = client.chat_completion(messages)
text = client.extract_response_text(response)
print(text)
```

### Async Usage

```python
from app.core.llm_client import chat_async

# Quick async chat
response = await chat_async([
    {"role": "user", "content": "Summarize this document..."}
])
print(response)
```

### Custom Parameters

```python
from app.core.llm_client import get_llm_client

client = get_llm_client()

# Override default parameters
response = client.chat_completion(
    messages=[...],
    temperature=0.7,  # More creative
    max_tokens=2000,  # Shorter response
    top_p=0.9
)
```

### Embeddings

```python
from app.core.llm_client import embed

# Get embeddings
text = "Regulatory compliance requirements"
embedding = embed(text)

# Batch embeddings
texts = ["Text 1", "Text 2", "Text 3"]
embeddings = embed(texts)
```

### With Agent Prompts

```python
from app.core.llm_client import get_llm_client
from app.agents.config.prompts import get_prompt

client = get_llm_client()

# Get prompt for specific agent
messages = client.format_prompt(
    system_prompt=get_prompt("compliance", "system"),
    user_message="Analyze regulatory update...",
    context="Document context here..."
)

response = client.chat_completion(messages)
```

---

## LLM Client API

### LLMClient Class

```python
class LLMClient:
    def __init__(self)
    def chat_completion(messages, model=None, temperature=None, ...)
    async def chat_completion_async(messages, ...)
    def get_embedding(text, model="text-embedding-3-small")
    async def get_embedding_async(text, ...)
    def format_prompt(system_prompt, user_message, context=None)
    def extract_response_text(response)
    def get_usage_stats(response)
    def get_model_info()
```

### Convenience Functions

```python
# Quick chat (returns text directly)
from app.core.llm_client import chat, chat_async

text = chat(messages)
text = await chat_async(messages)

# Quick embedding
from app.core.llm_client import embed

vector = embed("text to embed")
vectors = embed(["text1", "text2", "text3"])
```

---

## ChromaDB Integration

ChromaDB automatically uses the configured LLM provider for embeddings:

```python
from app.db.chroma_db import get_collection

# Collection automatically uses configured embeddings
collection = get_collection("regulatory_documents")

# Add documents (embeddings generated automatically)
collection.add(
    documents=["Document text..."],
    metadatas=[{"source": "FCA"}],
    ids=["doc1"]
)

# Query (uses same embeddings)
results = collection.query(
    query_texts=["What are MiFID requirements?"],
    n_results=5
)
```

### Embedding Function Priority

1. **Azure OpenAI** (if `LLM_PROVIDER=azure` and API key set)
2. **OpenAI** (if `LLM_PROVIDER=openai` and API key set)
3. **SentenceTransformers** (local fallback, no API key needed)

---

## Agent Integration

All AI agents use the centralized LLM client:

```python
from app.core.llm_client import get_llm_client
from app.agents.config.prompts import get_system_prompt

class ComplianceAgent:
    def __init__(self):
        self.llm = get_llm_client()
        self.system_prompt = get_system_prompt("compliance")

    async def analyze(self, document):
        messages = self.llm.format_prompt(
            system_prompt=self.system_prompt,
            user_message=f"Analyze: {document}"
        )
        
        response = await self.llm.chat_completion_async(messages)
        return self.llm.extract_response_text(response)
```

---

## Model Selection

### Azure OpenAI Models

Available models (check your deployment):
- `gpt-4.1` - Latest GPT-4 (recommended)
- `gpt-4-turbo` - Fast GPT-4
- `gpt-4-32k` - Large context
- `gpt-35-turbo` - Cost-effective

### OpenAI Models

Available models:
- `gpt-4-turbo-preview` - Latest GPT-4
- `gpt-4` - Standard GPT-4
- `gpt-4-32k` - Large context
- `gpt-3.5-turbo` - Fast and cheap

### Embedding Models

- **Azure**: Uses deployment name (same as chat)
- **OpenAI**: `text-embedding-3-small`, `text-embedding-3-large`
- **Local**: `all-MiniLM-L6-v2` (SentenceTransformers)

---

## Temperature Guide

Temperature controls randomness:

| Temperature | Use Case | Example |
|-------------|----------|---------|
| 0.0 - 0.3 | Deterministic, factual | Requirements extraction, code generation |
| 0.4 - 0.7 | Balanced | Analysis, summarization |
| 0.8 - 1.2 | Creative | Brainstorming, ideation |
| 1.3 - 2.0 | Very creative | Creative writing (rarely used) |

**Default: 0.1** - Optimal for regulatory compliance (consistent, factual)

---

## Cost Optimization

### Token Management

```python
# Get usage statistics
response = client.chat_completion(messages)
stats = client.get_usage_stats(response)

print(f"Prompt tokens: {stats['prompt_tokens']}")
print(f"Completion tokens: {stats['completion_tokens']}")
print(f"Total tokens: {stats['total_tokens']}")
```

### Best Practices

1. **Limit max_tokens**: Set appropriate limits
   ```python
   response = client.chat_completion(messages, max_tokens=500)
   ```

2. **Use lower temperature**: More deterministic = fewer retries
   ```python
   response = client.chat_completion(messages, temperature=0.1)
   ```

3. **Cache results**: Store frequent queries
   ```python
   # Implement caching for repeated queries
   ```

4. **Batch processing**: Process multiple items together
   ```python
   # Process multiple documents in one call
   ```

---

## Error Handling

```python
from app.core.llm_client import get_llm_client

client = get_llm_client()

try:
    response = client.chat_completion(messages)
    text = client.extract_response_text(response)
except openai.RateLimitError:
    # Rate limit exceeded
    print("Rate limit exceeded, retry later")
except openai.APIError as e:
    # API error
    print(f"API error: {e}")
except Exception as e:
    # Other errors
    print(f"Error: {e}")
```

---

## Testing

### Test Azure OpenAI Connection

```bash
cd backend
python -c "
from app.core.llm_client import get_llm_client

client = get_llm_client()
info = client.get_model_info()
print('Provider:', info['provider'])
print('Endpoint:', info['endpoint'])
print('Model:', info['model_name'])

response = client.chat_completion([
    {'role': 'user', 'content': 'Say hello'}
])
print('Response:', client.extract_response_text(response))
"
```

### Test Embeddings

```bash
python -c "
from app.core.llm_client import embed

vector = embed('test text')
print(f'Embedding dimension: {len(vector)}')
print(f'First 5 values: {vector[:5]}')
"
```

### Test ChromaDB Integration

```bash
python -c "
from app.db.chroma_db import get_embedding_function

ef = get_embedding_function()
print('Embedding function:', type(ef).__name__)
"
```

---

## Troubleshooting

### Issue: "AZURE_OPENAI_API_KEY is required"

**Solution**: Set the API key in `.env` file:
```bash
AZURE_OPENAI_API_KEY=your-key-here
```

### Issue: "Invalid API endpoint"

**Solution**: Verify endpoint URL format:
```bash
# Correct format
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Remove /openai/deployments/... from the end
```

### Issue: "Deployment not found"

**Solution**: Verify deployment name matches Azure portal:
```bash
AZURE_OPENAI_DEPLOYMENT=gpt-4.1  # Must match exactly
```

### Issue: "API version not supported"

**Solution**: Use latest stable version:
```bash
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### Issue: Embeddings not working

**Solution**: Check ChromaDB logs:
```bash
tail -f storage/logs/application/app.log | grep embedding
```

---

## Security Best Practices

### 1. Never Commit API Keys
```bash
# .gitignore already includes .env files
echo ".env" >> .gitignore
```

### 2. Use Environment Variables
```bash
# Never hardcode keys in code
# Always use settings
from app.core.config import settings
api_key = settings.AZURE_OPENAI_API_KEY
```

### 3. Rotate Keys Regularly
- Rotate API keys every 90 days
- Use Azure Key Vault for production
- Monitor usage for anomalies

### 4. Implement Rate Limiting
```python
# Already implemented in config
RATE_LIMIT_ENABLED=True
MAX_REQUESTS_PER_MINUTE=60
```

---

## Migration Guide

### From OpenAI to Azure OpenAI

1. **Get Azure OpenAI credentials**
   - Create Azure OpenAI resource
   - Deploy model (e.g., gpt-4.1)
   - Get endpoint and API key

2. **Update .env file**
   ```bash
   # Change provider
   LLM_PROVIDER=azure
   
   # Add Azure credentials
   AZURE_OPENAI_ENDPOINT=https://...
   AZURE_OPENAI_API_KEY=...
   AZURE_OPENAI_DEPLOYMENT=gpt-4.1
   ```

3. **Restart application**
   ```bash
   python app.py
   ```

4. **Verify connection**
   ```python
   from app.core.llm_client import get_llm_client
   client = get_llm_client()
   print(client.get_model_info())
   ```

**No code changes required!** The LLM client automatically detects the provider.

---

## Performance Tips

1. **Use streaming for long responses**
   ```python
   response = client.chat_completion(messages, stream=True)
   for chunk in response:
       print(chunk.choices[0].delta.content)
   ```

2. **Implement caching**
   ```python
   # Cache frequent queries
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_cached_response(query):
       return client.chat_completion([...])
   ```

3. **Batch process when possible**
   ```python
   # Process multiple items together
   batch_messages = [...]
   response = client.chat_completion(batch_messages)
   ```

---

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) - System validation
- [backend/app/agents/config/prompts.py](backend/app/agents/config/prompts.py) - Agent prompts
- [backend/app/core/llm_client.py](backend/app/core/llm_client.py) - LLM client implementation

---

**Last Updated**: 2026-04-02  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
