# Bottega mandatory security standard

Every line of code, configuration or infrastructure the team produces must meet this standard. The baseline is **OWASP ASVS level 2**, supplemented by the OWASP Top 10, the OWASP API Security Top 10 and, when the application uses language models, the OWASP Top 10 for LLM Applications. When the system processes personal data of people in the EU, **GDPR** applies.

Rules marked **[MUST]** allow no exceptions. A violation is always a `BLOCKER` finding.

## 1. Principles
- **Secure by default:** the default configuration is the restrictive one. Whatever is needed gets opened explicitly.
- **Least privilege:** users, services, tokens, containers and cloud roles get only the permissions they need.
- **Defense in depth:** never rely on a single control (e.g. validate on the client *and* the server).
- **Fail closed:** when a security control errors, access is denied.
- **All input is hostile:** users, external APIs, files, headers, environment variables, LLM output.
- **Don't roll your own crypto or authentication:** use established libraries and providers.

## 2. Input validation and output encoding
- [MUST] Validate every input on the server against an explicit schema (type, length, format, range), using allow-lists.
- [MUST] Encode output for its context (HTML, attribute, JS, URL). Never disable the framework's auto-escaping, and never use `innerHTML`, `dangerouslySetInnerHTML`, `v-html` or equivalents with unsanitized data.
- Limit the size of request bodies, uploads and arrays, and the depth of JSON.

## 3. Injection
- [MUST] SQL and NoSQL queries are parameterized or built with an ORM or query builder. Never concatenate input into a query string.
- [MUST] No `eval`, `exec`, `Function()` or unsafe deserialization (`pickle`, unsafe `yaml.load`, `ObjectInputStream`) on untrusted data.
- [MUST] For system commands, use argument-list APIs (`subprocess.run([...])`, `execFile`), never a shell with interpolated strings.
- Prevent path traversal: normalize paths and verify they stay inside the intended directory.
- Prevent SSRF: for user-supplied URLs, use a host allow-list, block private, link-local and metadata IPs (169.254.169.254), and never follow redirects blindly.

## 4. Authentication and sessions
- Prefer an established identity provider (OIDC/OAuth 2.1 with PKCE) over a home-grown login system.
- [MUST] If you store passwords, hash them with **Argon2id** (or bcrypt with cost ≥ 12, or scrypt). Never MD5, SHA-1, unsalted SHA-256 or reversible encryption.
- [MUST] Rate limiting and progressive delays on login, sign-up, password reset and OTP.
- Support MFA for privileged accounts. Check passwords against breached-password lists and require at least 12 characters, with no arbitrary composition rules.
- [MUST] Session cookies are `HttpOnly`, `Secure` and `SameSite=Lax` or `Strict`. Regenerate the session ID on login, and invalidate the session on logout and on password change.
- JWTs have their signature verified with a fixed algorithm (never `none`), a short expiry, and verified audience and issuer. They carry no sensitive data.
- Login error messages do not reveal whether the user exists.

## 5. Authorization
- [MUST] Deny by default. Every endpoint states explicitly who may access it.
- [MUST] Check authorization on the server for every request, **at object level**: the user may access *this* resource, not just this type of resource (against IDOR and BOLA).
- [MUST] Prevent mass assignment: writable fields are an explicit allow-list.
- Authorization logic is centralized and tested with negative cases (user A cannot see user B's data).

## 6. Secrets
- [MUST] No secrets (passwords, API keys, tokens, private keys, connection strings with credentials) in code, tests, logs, commit messages, Docker images or versioned files.
- [MUST] Secrets come from environment variables or a secret manager. The repository contains only `.env.example` with placeholder values, and `.env*` is in `.gitignore`.
- In CI, use the platform's secret store and, where possible, federated credentials (OIDC) instead of static keys.
- Every secret has a rotation plan documented in `docs/09-release.md`.

## 7. Cryptography
- [MUST] TLS 1.2 or higher for all network traffic. HSTS enabled in production. Never disable certificate verification (`verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify`).
- [MUST] For security-relevant randomness (tokens, unguessable IDs, salts), use a CSPRNG (`secrets`, `crypto.randomBytes`, `crypto/rand`), never `Math.random` or `random`.
- Symmetric encryption uses AES-256-GCM or ChaCha20-Poly1305, through high-level libraries (libsodium, `cryptography`, Web Crypto).
- Sensitive data at rest is encrypted: encrypted database, encrypted backups, and field-level encryption for the most sensitive data.

## 8. Data protection and privacy (GDPR)
- Every piece of personal data is classified in `docs/05-data.md` (public, internal, personal, special category under Art. 9), with its purpose and retention period.
- **Data minimization:** collect only what a requirement needs.
- Support exporting and deleting a user's data (rights of access, portability and erasure), and automatic cleanup of expired data.
- No real personal data in development or test environments. Use synthetic data.

## 9. Error handling and logging
- [MUST] Users get generic errors. Stack traces, queries and internal paths stay on the server. Debug mode is off in production.
- [MUST] Logs contain no secrets, tokens, passwords, card numbers or unnecessary personal data. Mask what you must log.
- Log security events (successful and failed logins, permission changes, denied access, admin operations) with a timestamp, actor and correlation ID, in a structured format.
- Prevent log injection by neutralizing newline characters in input.

## 10. Web and API security
- Headers: a restrictive `Content-Security-Policy` (no `unsafe-inline` or `unsafe-eval` if avoidable), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `frame-ancestors` or `X-Frame-Options`, and `Strict-Transport-Security`.
- [MUST] CSRF protection for state-changing requests authenticated by cookie.
- [MUST] CORS with an explicit allow-list of origins. Never `*` together with credentials.
- Uploads: check the real type (magic bytes) and extension, enforce size limits, rename files, store them outside the web root or in private object storage, and scan them if possible.
- APIs: rate limiting, mandatory pagination, an OpenAPI schema as the contract, versioning, and responses without internal fields.

## 11. Dependencies and supply chain
- [MUST] Versions pinned with a committed lockfile.
- [MUST] Before adding a dependency, verify that it exists on the official registry under the exact name, that it is maintained, that its license is compatible, and that it has no known critical CVEs. Include this check in the report.
- Prefer the standard library, or a few established dependencies, over many small ones.
- In CI, pin GitHub Actions (or equivalents) to a commit SHA, give the CI token minimal permissions, and never expose secrets to pull requests from forks.

## 12. Containers and infrastructure
- Minimal images with pinned versions (distroless, slim or alpine), multi-stage builds, [MUST] a non-root user, a read-only filesystem where possible, and no secrets in layers.
- Infrastructure as code (Terraform, Pulumi, Bicep…) gets reviewed like application code. No public buckets, security groups open to `0.0.0.0/0` only on the intended public ports, and databases never exposed to the Internet.
- Automatic, encrypted backups with a tested restore.

## 13. LLM-powered applications (if applicable)
- Model output is untrusted input: validate it before using it in queries, commands, HTML or tool calls.
- Defend against direct and indirect prompt injection (documents, web pages, emails): separate instructions from data, limit tool permissions, and require human confirmation for irreversible actions.
- No secrets in system prompts. Cap tokens and cost per user.

## 14. Recommended verification tools
| Purpose | Tools (pick by stack) |
|---|---|
| Secrets | `gitleaks detect`, `trufflehog` |
| SAST | `semgrep --config auto` (or `p/owasp-top-ten`), `bandit` (Python), `eslint-plugin-security`, `gosec` |
| Dependencies | `npm audit`, `pnpm audit`, `pip-audit`, `osv-scanner`, `cargo audit`, `govulncheck` |
| Containers and IaC | `trivy image`, `trivy config`, `checkov`, `hadolint` |
| DAST | OWASP ZAP baseline scan against the staging environment |

If a tool is not installed, the security engineer reports it and proposes how to install it, and does not declare the check passed without running it.
