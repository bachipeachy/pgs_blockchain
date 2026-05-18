# IN_WALLET_CREATED_V0

## Header (Mandatory)

- **Artifact Code:** IN_WALLET_CREATED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_CREATE_WALLET_V0

---

## 1. Intent

Create a wallet for a verified actor, establishing their financial account within the system.

---

## 2. Rationale

Wallet creation requires:
- Actor must be resolved (verified)
- Wallet ID is deterministically generated
- Wallet record is persisted with event trail

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_CREATE_WALLET_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor identity data (first_name, last_name, email_registration) |
| wallet_type | string | false | Type of wallet to create (default: standard) |
| wallet_config | object | false | Optional configuration for the wallet (name, currency, metadata) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Wallet creation initiated |
| NACK | Wallet creation failed |

---

## 6. Domain

- **Domain:** pgs.finance.wallet

---

## Machine

```yaml
in_code: IN_WALLET_CREATED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Create wallet for verified actor
  workflow: WF_CREATE_WALLET_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Actor identity data (first_name, last_name, email_registration)
    wallet_type:
      type: string
      default: standard
      description: Type of wallet to create
    wallet_config:
      type: object
      description: Optional configuration for the wallet (name, currency, metadata)

  outcomes:
    ACK:
      description: Wallet creation initiated
    NACK:
      description: Wallet creation failed

extensions:
  domain: pgs.finance.wallet
```
