# EV_TRANSACTION_SUBMITTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_TRANSACTION_SUBMITTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A transaction has been signed and persisted to the local mempool.

---

## 2. Rationale

This event records successful transaction submission:
- Links transaction to wallet and actor
- Provides transaction hash for tracking
- Enables audit of transaction lifecycle

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_SUBMIT_TRANSACTION_V0 | CC_APPEND_TX_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_id | string | true | Transaction identifier |
| tx_hash | string | true | Transaction hash |
| wallet_id | string | true | Source wallet |
| from_address | string | true | Sender address |
| to_address | string | true | Destination address |
| value | string | true | Transfer value in wei |
| status | string | true | Transaction status (PENDING) |
| timestamp | string (date-time) | true | When transaction was submitted |

---

## Machine

```yaml
ev_code: EV_TRANSACTION_SUBMITTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Transaction signed and persisted to mempool
  description: Emitted after a transaction is successfully signed, persisted to the mempool, and indexed

  schema:
    tx_id:
      type: string
      required: true
    tx_hash:
      type: string
      required: true
    wallet_id:
      type: string
      required: true
    from_address:
      type: string
      required: true
    to_address:
      type: string
      required: true
    value:
      type: string
      required: true
    status:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
