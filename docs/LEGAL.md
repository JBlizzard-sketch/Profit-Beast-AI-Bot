# Legal & KYC Template (Draft)

**AltTrade AI Bot (ProfitBeast Edition)** — Legal and Compliance Notes

1. No financial advice
   - The bot provides signals and trading tools. Users accept that these are informational only and not financial advice.

2. KYC & AML
   - For live trading and payment processing, require user identity verification.
   - Suggested KYC flow:
     1. Collect full name, DOB, country
     2. Government ID upload
     3. Selfie + liveness check
     4. Address verification
   - Store KYC approvals in a secure database and mark accounts in `users.is_premium` only after verification.

3. Terms & Conditions
   - Users must accept T&Cs on first use. Implement acceptance flag in users table.

4. Data privacy
   - Do not store secrets in code. Use env vars and secret managers in production.
   - Provide data deletion and export endpoints for GDPR compliance.

5. Liability
   - Include disclaimers and limit of liability clauses.

This document is a template. Consult legal counsel for production use.
