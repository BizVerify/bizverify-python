# BizVerify Python SDK

Official Python SDK for the [BizVerify](https://bizverify.co) business entity verification API.

## Installation

```bash
pip install bizverify
```

## Quick Start

### Authentication (Passwordless)

```python
from bizverify import BizVerify

client = BizVerify()

# Request a verification code via email
client.auth.request_access("you@example.com", accept_terms=True)

# Verify the code — client is automatically configured with the new API key
resp = client.auth.verify_access("you@example.com", "123456", label="my-agent")
print(resp.api_key)  # Store this for future use

# Or initialize with an existing API key
client = BizVerify(api_key="bv_live_...")
```

### Verify a Business Entity

```python
client = BizVerify(api_key="bv_live_...")

# Synchronous verification (cached result)
result = client.verification.verify("Acme Inc", "us-fl")
print(result.status, result.data)

# Verify and wait for async job to complete
job = client.verification.verify_and_wait("Acme Inc", "us-fl")
print(job.status, job.result)
```

### Search for Entities

```python
# Single page
response = client.search.find("Acme", jurisdiction="us-fl")
for result in response.results:
    print(result.entity_name, result.confidence)

# Auto-paginate through all results
for result in client.search.find_all("Acme"):
    print(result.entity_name)
```

### Response Metadata

Every API call populates `last_response_meta` with credit and rate limit info:

```python
result = client.verification.verify("Acme Inc", "us-fl")
meta = client.last_response_meta
print(meta.credits_remaining)    # 85
print(meta.credits_charged)      # 15
print(meta.rate_limit_remaining)  # 59
```

### Configuration & Jurisdictions

```python
# Get full API configuration (no auth required)
config = client.config.get()
print(config.pricing)
print(config.jurisdictions)

# List supported jurisdictions
resp = client.config.jurisdictions()
for j in resp.jurisdictions:
    print(j.code, j.name, j.features)
```

### Async Client

```python
import asyncio
from bizverify import AsyncBizVerify

async def main():
    async with AsyncBizVerify(api_key="bv_live_...") as client:
        result = await client.verification.verify("Acme Inc", "us-fl")
        print(result.status)

        async for result in client.search.find_all("Acme"):
            print(result.entity_name)

asyncio.run(main())
```

### Error Handling

```python
from bizverify import BizVerify, NotFoundError, InsufficientCreditsError, RateLimitError

client = BizVerify(api_key="bv_live_...")

try:
    entity = client.entities.get("ent_nonexistent")
except NotFoundError as e:
    print(f"Not found: {e.message} (code={e.code})")
except InsufficientCreditsError:
    print("Need more credits")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

## API Reference

### Resources

| Resource | Methods |
|----------|---------|
| `client.auth` | `request_access()`, `verify_access()` |
| `client.verification` | `verify()`, `verify_and_wait()`, `get_status()` |
| `client.entities` | `get()`, `history()` |
| `client.search` | `find()`, `find_all()` |
| `client.account` | `get()`, `usage()`, `data_export()`, `update_email()`, `create_key()`, `revoke_key()` |
| `client.billing` | `get()`, `purchase()` |
| `client.config` | `get()`, `jurisdictions()` |
| `client.checker` | `check()` |

### Client Options

```python
client = BizVerify(
    api_key="bv_live_...",      # API key authentication
    base_url="https://...",     # Custom base URL
    max_retries=2,              # Retry on 5xx (default: 2)
    timeout=30.0,               # Request timeout in seconds (default: 30)
)
```

## Requirements

- Python >= 3.9
- httpx >= 0.25

## License

MIT
