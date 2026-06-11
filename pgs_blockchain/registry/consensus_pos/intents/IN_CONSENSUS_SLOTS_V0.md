# IN_CONSENSUS_SLOTS_V0

## Header (Mandatory)

- **Artifact Code:** IN_CONSENSUS_SLOTS_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_RUN_CONSENSUS_SLOTS_V0

---

## 1. Intent

Initiate a finite ordered consensus slot run. Validates that the slot schedule is a non-empty array of slot descriptors and that a triggering actor is identified.

---

## 2. Rationale

WF_RUN_CONSENSUS_SLOTS_V0 requires a non-empty, ordered list of slot descriptors — each containing the transaction workload and block proposal parameters for one slot. The intent enforces this precondition at the boundary before any CC executes. The slot_schedule must be non-empty because CC_EXECUTE_SLOT_SEQUENCE_V0 (Collatz pattern) guarantees termination only for finite, non-empty arrays. An empty array at admission is a caller error, not a runtime condition.

Each slot descriptor carries: slot number, epoch, round number, timestamp, and a transactions array. Deep validation of individual transaction descriptor fields occurs within the typed WF intents invoked per transaction during slot execution, not at this intent.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_RUN_CONSENSUS_SLOTS_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| slot_schedule | array | true | Non-empty ordered list of slot descriptors; each describes one slot's workload |
| triggered_by | string | true | actor_id of the system actor initiating the slot run |

**Slot descriptor shape** (each element of slot_schedule):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| slot | integer | true | Slot number within epoch (≥ 0) |
| epoch | integer | true | Epoch number (≥ 0) |
| round_number | integer | true | Global consensus round number (≥ 0) |
| timestamp | string | true | ISO 8601 timestamp for this slot |
| transactions | array | true | Ordered list of transaction descriptors for this slot (may be empty) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Payload admitted — slot_schedule is a non-empty array; triggered_by is present |
| NACK | Payload rejected — slot_schedule missing, empty, or not an array; triggered_by missing |

---

## 6. Domain

- **Domain:** pgs.consensus_pos.slot_execution
- **Notes:**
  - slot_schedule must be non-empty (minItems: 1) — empty array is caller error
  - triggered_by must be a non-empty string; actor existence not validated at intent admission
  - Per-slot transaction descriptor field validation occurs in typed WF intents at execution time
  - Termination guarantee for CC_EXECUTE_SLOT_SEQUENCE_V0 depends on finite non-empty slot_schedule

---

## Machine

```yaml
in_code: IN_CONSENSUS_SLOTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Initiate a finite consensus slot run
  workflow: WF_RUN_CONSENSUS_SLOTS_V0

  inputs:
    slot_schedule:
      type: array
      required: true
      minItems: 1
      description: Non-empty ordered list of slot descriptors
      items:
        type: object
        required: [slot, epoch, round_number, timestamp, transactions]
        properties:
          slot:
            type: integer
            minimum: 0
          epoch:
            type: integer
            minimum: 0
          round_number:
            type: integer
            minimum: 0
          timestamp:
            type: string
            format: date-time
          transactions:
            type: array
    triggered_by:
      type: string
      required: true
      description: actor_id of the system actor initiating the slot run

  outcomes:
    ACK:
      description: Payload admitted — slot_schedule is non-empty array; triggered_by present
    NACK:
      description: Payload rejected — slot_schedule missing/empty/non-array or triggered_by missing

extensions:
  domain: pgs.consensus_pos.slot_execution
  notes:
    - slot_schedule minItems: 1 — empty array is caller error; enforced at admission
    - Termination guarantee for CC_EXECUTE_SLOT_SEQUENCE_V0 (Collatz) depends on finite non-empty slot_schedule
    - triggered_by actor existence not validated at intent admission
    - Per-transaction field validation occurs in typed WF intents (WF_SUBMIT_TRANSFER_V0, etc.) at execution time
    - transactions array within each slot descriptor may be empty (valid: slot with no transactions → only WF_PROPOSE_BLOCK_V0 invoked for that slot)
```
