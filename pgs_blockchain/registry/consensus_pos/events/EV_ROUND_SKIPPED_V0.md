# EV_ROUND_SKIPPED_V0

## Header (Mandatory)

- **Artifact Code:** EV_ROUND_SKIPPED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A consensus round was skipped due to no pending transactions.

---

## 2. Rationale

This event records a skipped round in the consensus lifecycle:
- Provides a complete audit record of all rounds, including empty ones
- Enables monitoring of validator liveness and network activity
- Preserves round_id continuity in the consensus journal

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_PROPOSE_BLOCK_V0 | CC_SKIP_ROUND_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_id | integer | true | Consensus round number that was skipped |
| proposer_id | string | true | actor_id of the selected proposer for this round |
| outcome | string | true | Always SKIPPED |
| timestamp | string (date-time) | true | When the skip was recorded |

---

## Machine

```yaml
ev_code: EV_ROUND_SKIPPED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Consensus round skipped — no pending transactions
  description: Emitted by CC_SKIP_ROUND_V0 when a consensus round produces no block due to an empty transaction pool

  schema:
    round_id:
      type: integer
      required: true
    proposer_id:
      type: string
      required: true
    outcome:
      type: string
      required: true
      enum: [SKIPPED]
    timestamp:
      type: string
      format: date-time
      required: true
```
