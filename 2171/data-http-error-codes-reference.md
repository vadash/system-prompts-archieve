<!--
name: 'Data: HTTP error codes reference'
description: >-
  Reference for HTTP error codes returned by the Claude API with common causes
  and handling strategies
ccVersion: 2.1.63
-->
# HTTP Error Codes Reference

| Code | Error Type | Retryable | Common Cause |
|------|------------|-----------|--------------|
| 400 | `invalid_request_error` | No | Invalid format/params (e.g. roles not alternating) |
| 401 | `authentication_error` | No | Invalid/missing API key |
| 403 | `permission_error` | No | Key lacks permission |
| 404 | `not_found_error` | No | Invalid endpoint/model ID |
| 413 | `request_too_large` | No | Request exceeds size limits |
| 429 | `rate_limit_error` | Yes | Exceeded RPM/TPM limits |
| 500 | `api_error` | Yes | Anthropic service issue |
| 529 | `overloaded_error` | Yes | API temporarily overloaded |

## Handling
- **SDKs auto-retry** 429 and 5xx errors by default.
- Always use typed exceptions (e.g. `Anthropic.RateLimitError`, `anthropic.APIError`) instead of string-matching error messages.
- Common 400 fix: Ensure `budget_tokens` < `max_tokens` (older models). For 4.6, don't use `budget_tokens` at all.