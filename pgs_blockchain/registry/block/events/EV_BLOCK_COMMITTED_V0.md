# EV_BLOCK_COMMITTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_BLOCK_COMMITTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A block has been committed to the canonical chain with its is_canonical flag set.

---

## 2. Rationale

Commitment is the canonical chain selection event:
- Marks the block record as canonical (is_canonical: true)
- Distinguishes canonical from orphaned blocks after fork resolution

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
| height | integer | true | Block height |
| is_canonical | boolean | true | Whether this block is on the canonical chain |
| timestamp | string (date-time) | true | When commitment was recorded |

---

## Machine

```yaml
ev_code: EV_BLOCK_COMMITTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Block committed to canonical chain
  description: Emitted when a block's canonical status is resolved; is_canonical true means the block is on the main chain

  schema:
    block_hash:
      type: string
      required: true
    height:
      type: integer
      required: true
    is_canonical:
      type: boolean
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
