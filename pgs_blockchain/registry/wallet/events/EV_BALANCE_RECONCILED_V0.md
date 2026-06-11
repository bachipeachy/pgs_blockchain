# EV_BALANCE_RECONCILED_V0

## Header (Mandatory)

- **Artifact Code:** EV_BALANCE_RECONCILED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A wallet's balance has been reconciled following transaction finalization.

---

## 2. Rationale

Balance reconciliation closes the wallet lifecycle loop after a finalized transaction:
- Records the before/after balance for audit
- Links the balance change to the transaction that caused it
- Enables wallet event stream reconstruction and audit trail

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| (consensus finalization CR — next CR) | (to be declared) |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| wallet_id | string | true | Wallet identifier |
| actor_id | string | true | Actor who owns this wallet |
| previous_balance | number | true | Balance before this transaction |
| delta | number | true | Signed balance change (positive = credit, negative = debit) |
| new_balance | number | true | Balance after this transaction |
| tx_hash | string | true | Transaction hash that caused this reconciliation |
| timestamp | string (date-time) | true | When reconciliation was recorded |

---

## Machine

```yaml
ev_code: EV_BALANCE_RECONCILED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Wallet balance reconciled after transaction finalization
  description: Emitted after a finalized transaction updates a wallet's balance; enables complete audit trail of balance changes

  schema:
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    previous_balance:
      type: number
      required: true
    delta:
      type: number
      required: true
    new_balance:
      type: number
      required: true
    tx_hash:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
