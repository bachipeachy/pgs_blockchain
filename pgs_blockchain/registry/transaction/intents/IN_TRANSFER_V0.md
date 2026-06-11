# IN_TRANSFER_V0

## Header (Mandatory)

- **Artifact Code:** IN_TRANSFER_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_TRANSFER_V0

---

## 1. Intent

Submit a TRANSFER transaction — send BACHI from one wallet to another.

---

## 2. Rationale

Typed transaction admission replaces the generic IN_TRANSACTION_SUBMITTED_V0.
Each transaction type carries its own schema, authority class, and auto-resolution rules.
TRANSFER is an ENDUSER operation: actor identity is required, from/to wallets are explicit.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_TRANSFER_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor record for identity resolution |
| actor_record.email_registration | string | true | Actor email (format: email) |
| from_wallet_id | string | true | Source wallet identifier |
| to_address | string | true | Destination wallet address (0x-prefixed) |
| amount | number | true | Transfer amount in BACHI |
| gas_limit | integer | false | Gas limit (default 21000) |
| max_fee_per_gas | string | false | Max fee per gas in wei (default "20000000000") |
| max_priority_fee_per_gas | string | false | Max priority fee per gas in wei (default "1000000000") |
| memo | string | false | Optional transaction memo |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Transfer intent accepted |
| NACK | Transfer intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** ENDUSER

---

## Machine

```yaml
in_code: IN_TRANSFER_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit TRANSFER transaction (ENDUSER)
  workflow: WF_TRANSFER_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Actor record for identity resolution
      fields:
        email_registration:
          type: string
          required: true
          format: email
    from_wallet_id:
      type: string
      required: true
      description: Source wallet identifier
    to_address:
      type: string
      required: true
      description: Destination wallet address (0x-prefixed)
    amount:
      type: number
      required: true
      description: Transfer amount in BACHI
    gas_limit:
      type: integer
      default: 21000
      description: Gas limit
    max_fee_per_gas:
      type: string
      default: "20000000000"
      description: Max fee per gas in wei
    max_priority_fee_per_gas:
      type: string
      default: "1000000000"
      description: Max priority fee per gas in wei
    memo:
      type: string
      required: false
      description: Optional transaction memo

  outcomes:
    ACK:
      description: Transfer intent accepted
    NACK:
      description: Transfer intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: ENDUSER
```
