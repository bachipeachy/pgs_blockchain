# CC_SKIP_ROUND_V0

## Header (Mandatory)

- **Artifact Code:** CC_SKIP_ROUND_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_ASSEMBLE_RECORD_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Record a skipped consensus round to the CONSENSUS_ROUNDS and CONSENSUS_EVENTS stores when no pending transactions are available for block assembly.

---

## 2. Rationale

Round continuity requires that every consensus round — including empty ones — is recorded in the append-only journal. Skipping round records would create gaps in the consensus audit trail. All writes are scoped to consensus_pos stores only.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_ASSEMBLE_RECORD_V0 | CT | Assemble skip_record |
| 2 | CS_APPENDONLY_JSONL_V0 | CS | APPEND to CONSENSUS_ROUNDS |
| 3 | CS_APPENDONLY_JSONL_V0 | CS | APPEND to CONSENSUS_EVENTS |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_id | integer | true | Consensus round number being skipped |
| proposer_id | string | true | actor_id of the selected proposer for this round |
| timestamp | string | true | ISO 8601 timestamp of the skip |

---

## 5. Outputs

No outputs. This CC records state as side effects only.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Skip record written to both stores |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION on missing or invalid required inputs
- BACKEND_ERROR propagates as a hard failure from any CS step

---

## Machine

```yaml
cc_code: CC_SKIP_ROUND_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Record a skipped consensus round to CONSENSUS_ROUNDS and CONSENSUS_EVENTS

  inputs:
    round_id:
      type: integer
      required: true
    proposer_id:
      type: string
      required: true
    timestamp:
      type: string
      required: true
      format: date-time

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: assemble_skip_record
      transform: capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0
      inputs:
        fields:
          round_id: $.inputs.round_id
          proposer_id: $.inputs.proposer_id
          outcome: SKIPPED
          timestamp: $.inputs.timestamp
      outputs:
        skip_record: $.capability_result.record
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: append_to_rounds
        VIOLATION: exit

    - step: append_to_rounds
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: CONSENSUS_ROUNDS
      op: APPEND
      inputs:
        stream_id: $.inputs.round_id
        record: $.results.assemble_skip_record.skip_record
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: append_to_events
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: append_to_events
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: CONSENSUS_EVENTS
      op: APPEND
      inputs:
        stream_id: $.inputs.round_id
        record:
          event_code: EV_ROUND_SKIPPED_V0
          round_id: $.inputs.round_id
          proposer_id: $.inputs.proposer_id
          outcome: SKIPPED
          timestamp: $.inputs.timestamp
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: consensus_pos
  notes:
    - All writes scoped to consensus_pos stores (CONSENSUS_ROUNDS, CONSENSUS_EVENTS)
    - No cross-subdomain writes
```
