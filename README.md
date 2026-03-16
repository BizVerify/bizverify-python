# BizVerify Python SDK

Official Python SDK for the [BizVerify](https://bizverify.co) business entity verification API.

## Installation

```bash
pip install bizverify
```

## Quick Start

### Verify a Business Entity

```python
from bizverify import BizVerify

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

### Authentication (JWT)

```python
client = BizVerify()

# Register
reg = client.auth.register("user@example.com", "password123", accept_terms=True)
print(reg.api_key)  # Store this

# Login (auto-stores JWT token)
login = client.auth.login("user@example.com", "password123")

# Now JWT-authenticated endpoints work
account = client.account.get()
print(account.credit_balance)
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
| `client.auth` | `register()`, `login()`, `verify_email()`, `resend_verification()`, `forgot_password()`, `reset_password()` |
| `client.verification` | `verify()`, `verify_and_wait()`, `get_status()` |
| `client.entities` | `get()`, `history()` |
| `client.search` | `find()`, `find_all()` |
| `client.account` | `get()`, `usage()`, `data_export()`, `update_email()`, `update_password()`, `delete()`, `create_key()`, `revoke_key()` |
| `client.billing` | `get()`, `purchase()` |
| `client.checker` | `check()` |

### Client Options

```python
client = BizVerify(
    api_key="bv_live_...",      # API key authentication
    token="eyJ...",             # JWT authentication
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
