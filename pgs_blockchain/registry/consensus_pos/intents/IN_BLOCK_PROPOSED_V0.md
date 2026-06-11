# IN_BLOCK_PROPOSED_V0

## Header (Mandatory)

- **Artifact Code:** IN_BLOCK_PROPOSED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** WF_PROPOSE_BLOCK_V0

---

## 1. Intent

Initiate a consensus proposer selection and block formation round for a given round number.

---

## 2. Rationale

Block proposal is triggered externally by a consensus driver supplying a round number, a triggering actor, and the round timestamp. The intent validates these three required fields before admitting the payload to WF_PROPOSE_BLOCK_V0. Timestamp is carried in the intent so that all downstream CCs (CC_FORM_BLOCK_V0, CC_SKIP_ROUND_V0, CC_RECORD_CONSENSUS_ROUND_V0) write consistent time data without each independently sourcing a timestamp.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_PROPOSE_BLOCK_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_number | integer | true | Non-negative consensus round number |
| triggered_by | string | true | actor_id of the consensus driver triggering this round |
| slot | integer | true | Slot within epoch; equals round_number % 32; supplied by CC_EXECUTE_SLOT_SEQUENCE_V0 |
| epoch | integer | true | Epoch number; equals round_number // 32; supplied by CC_EXECUTE_SLOT_SEQUENCE_V0 |
| timestamp | string | true | ISO 8601 timestamp of round initiation |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Payload admitted — all five required fields present and valid |
| NACK | Payload rejected — missing required fields or round_number negative |

---

## 6. Domain

- **Domain:** pgs.consensus_pos.block_proposal
- **Notes:**
  - round_number must be a non-negative integer (≥ 0); rounds are zero-indexed
  - timestamp is carried through to all downstream CCs for consistent event timestamping
  - triggered_by must be a valid actor_id string; actor existence is not validated at intent admission

---

## Machine

```yaml
in_code: IN_BLOCK_PROPOSED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Initiate a consensus block proposal round
  workflow: WF_PROPOSE_BLOCK_V0

  inputs:
    round_number:
      type: integer
      required: true
      minimum: 0
      description: Non-negative consensus round number
    triggered_by:
      type: string
      required: true
      description: actor_id of the consensus driver triggering this round
    slot:
      type: integer
      required: true
      minimum: 0
      description: Slot within epoch; equals round_number % 32; supplied by CC_EXECUTE_SLOT_SEQUENCE_V0
    epoch:
      type: integer
      required: true
      minimum: 0
      description: Epoch number; equals round_number // 32; supplied by CC_EXECUTE_SLOT_SEQUENCE_V0
    timestamp:
      type: string
      required: true
      format: date-time
      description: ISO 8601 timestamp of round initiation

  outcomes:
    ACK:
      description: Payload admitted — all five required fields present and valid
    NACK:
      description: Payload rejected — missing required fields or round_number negative

extensions:
  domain: pgs.consensus_pos.block_proposal
  notes:
    - round_number minimum is 0 (rounds are zero-indexed)
    - slot and epoch are caller-supplied by CC_EXECUTE_SLOT_SEQUENCE_V0 from the slot descriptor
    - timestamp carried through to CC_FORM_BLOCK_V0, CC_SKIP_ROUND_V0, CC_RECORD_CONSENSUS_ROUND_V0
    - triggered_by actor existence not validated at intent admission
```
