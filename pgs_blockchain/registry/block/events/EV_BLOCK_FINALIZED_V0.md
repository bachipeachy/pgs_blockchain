# EV_BLOCK_FINALIZED_V0

## Header (Mandatory)

- **Artifact Code:** EV_BLOCK_FINALIZED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A block has been finalized — it is irreversible and part of the canonical chain.

---

## 2. Rationale

Finalization is the terminal lifecycle event for a block:
- Marks the block as irreversible
- Records the finalized epoch and included transaction count
- Triggers downstream balance reconciliation events

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| (consensus finalization CR — next CR) | (to be declared) |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| block_hash | string | true | Block identifier (BLK-prefixed) |
| height | integer | true | Block height in the canonical chain |
| slot | integer | true | Slot number within the epoch |
| epoch | integer | true | Epoch number |
| finalized_epoch | integer | true | Epoch at which finality was achieved |
| transaction_count | integer | true | Number of transactions included in the block |
| timestamp | string (date-time) | true | When finalization was recorded |

---

## Machine

```yaml
ev_code: EV_BLOCK_FINALIZED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Block finalized and added to canonical chain
  description: Emitted when a block achieves finality; signals that included transactions are irreversible

  schema:
    block_hash:
      type: string
      required: true
    height:
      type: integer
      required: true
    slot:
      type: integer
      required: true
    epoch:
      type: integer
      required: true
    finalized_epoch:
      type: integer
      required: true
    transaction_count:
      type: integer
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
