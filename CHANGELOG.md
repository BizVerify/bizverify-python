# Changelog

## 0.1.0 (2026-03-23)

- Initial release
- Full coverage of BizVerify public API (auth, verification, search, entities, account, billing, checker, config)
- Sync and async clients (`BizVerify`, `AsyncBizVerify`)
- Typed dataclass models (frozen/immutable) with `from_dict()` factories
- Exception hierarchy mapping all API error codes
- Job polling with exponential backoff (`verify_and_wait`)
- Auto-pagination for search results (`find_all`)
- Response metadata tracking (credits, rate limits)
- PEP 561 typed package (`py.typed`)
- Zero required dependencies beyond `httpx`
