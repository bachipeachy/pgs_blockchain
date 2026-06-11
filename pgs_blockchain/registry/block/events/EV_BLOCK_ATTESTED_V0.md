# EV_BLOCK_ATTESTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_BLOCK_ATTESTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A block has received attestations from validators in the consensus committee.

---

## 2. Rationale

Attestation events are the observable signal of consensus progress:
- Links attestation aggregate to the block and epoch
- Records the number of committee attestations received
- Enables finality tracking and fork-choice accounting

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
| slot | integer | true | Slot number within the epoch |
| epoch | integer | true | Epoch number |
| attestation_count | integer | true | Number of committee attestations received |
| timestamp | string (date-time) | true | When attestation aggregate was recorded |

---

## Machine

```yaml
ev_code: EV_BLOCK_ATTESTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Block received validator attestations
  description: Emitted when a block accumulates attestations; signals consensus progress toward finality

  schema:
    block_hash:
      type: string
      required: true
    slot:
      type: integer
      required: true
    epoch:
      type: integer
      required: true
    attestation_count:
      type: integer
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
