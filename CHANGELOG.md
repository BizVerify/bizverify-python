# Changelog

## 0.2.0 (2026-04-18)

- BREAKING: `verification_level` values renamed `pre_check` → `quick`, `full` → `deep`. Wire format JSON field name is unchanged; only the string values differ.
- Added `VerificationLevel` typed `Literal["quick", "deep"]` alias, exported from the top-level package.
- `verification.verify()` and `verification.verify_and_wait()` (sync + async) now accept `verification_level: VerificationLevel | None` for improved type-checker support.

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
