# LEXORA — CREDITS AND TRANSACTIONS

Create a Credits & Transactions page.

### Balance Overview

Display:
- Available credits.
- Reserved credits.
- Expiring credit lots.
- Top Up button.

### Credit Packages

Create configurable package cards.

Do not invent package names, prices, or credit amounts. Use placeholders that can be populated from server configuration.

### Transaction Ledger

Create a readable transaction table with:
- Transaction ID.
- Transaction source.
- Credit amount.
- Status.
- Created date.
- Expiry date when applicable.

### Checkout

Design a checkout flow showing:
- Selected package.
- Amount.
- Currency.
- Payment method.
- Payment status.

Include pending, paid, and failed states.

Important: Never display payment success based only on browser redirection. Payment success must be confirmed by the backend.

### Rewarded Ads

Rewarded ads are optional and login-only for the MVP.

Before an ad starts, show:
- Exact reward.
- Expiration.
- Non-transferability.
- Conditions.

Do not display rewarded ads to Guest users.

Do not make advertisements a blocking step in checkout or active AI jobs.