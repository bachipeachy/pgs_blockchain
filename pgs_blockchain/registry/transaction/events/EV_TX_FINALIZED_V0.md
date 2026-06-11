# EV_TX_FINALIZED_V0

## Header (Mandatory)

- **Artifact Code:** EV_TX_FINALIZED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A transaction has been finalized — it is included in a finalized block and its effects are irreversible.

---

## 2. Rationale

Transaction finalization closes the lifecycle loop for mempool entries:
- Links the transaction to its finalized block
- Records the effective fees paid
- Triggers downstream balance reconciliation for affected wallets

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| (consensus finalization CR — next CR) | (to be declared) |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_hash | string | true | Transaction hash (TX-prefixed) |
| tx_type | string | true | Transaction type (TRANSFER, STAKE, UNSTAKE, MINT, BURN, POOL, REWARD, SLASH) |
| from_address | string | true | Source wallet address |
| to_address | string | true | Destination wallet address |
| amount | number | true | Transaction amount in BACHI |
| total_fee | number | true | Total fee paid (gas_used × effective_gas_price) |
| block_hash | string | true | Block hash in which this transaction was finalized |
| timestamp | string (date-time) | true | When finalization was recorded |

---

## Machine

```yaml
ev_code: EV_TX_FINALIZED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Transaction finalized in a canonical block
  description: Emitted when a mempool transaction is included in a finalized block; signals that wallet balance changes are permanent

  schema:
    tx_hash:
      type: string
      required: true
    tx_type:
      type: string
      required: true
      enum: [TRANSFER, STAKE, UNSTAKE, MINT, BURN, POOL, REWARD, SLASH]
    from_address:
      type: string
      required: true
    to_address:
      type: string
      required: true
    amount:
      type: number
      required: true
    total_fee:
      type: number
      required: true
    block_hash:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
