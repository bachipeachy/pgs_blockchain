# EV_BLOCK_PROPOSED_V0

## Header (Mandatory)

- **Artifact Code:** EV_BLOCK_PROPOSED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A block has been formed and proposed for the current consensus round.

---

## 2. Rationale

This event records successful block formation:
- Links block to its consensus round and proposer
- Captures the set of transactions included in the block
- Enables audit of block lifecycle and chain construction

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_PROPOSE_BLOCK_V0 | CC_FORM_BLOCK_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| block_id | string | true | Block identifier (BLK-prefixed) |
| round_id | integer | true | Consensus round number that produced this block |
| proposer_id | string | true | actor_id of the validator that proposed the block |
| tx_ids | array | true | Ordered list of transaction IDs included in the block |
| timestamp | string (date-time) | true | When the block was formed |

---

## Machine

```yaml
ev_code: EV_BLOCK_PROPOSED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Block formed and proposed for consensus round
  description: Emitted by CC_FORM_BLOCK_V0 after a block is successfully formed and written to the BLOCKS store

  schema:
    block_id:
      type: string
      required: true
    round_id:
      type: integer
      required: true
    proposer_id:
      type: string
      required: true
    tx_ids:
      type: array
      required: true
      items:
        type: string
    timestamp:
      type: string
      format: date-time
      required: true
```
