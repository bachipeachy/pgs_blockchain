# CC_RECORD_CONSENSUS_ROUND_V0

## Header (Mandatory)

- **Artifact Code:** CC_RECORD_CONSENSUS_ROUND_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_ASSEMBLE_RECORD_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Record the PROPOSED outcome for a consensus round to the CONSENSUS_ROUNDS store after a block has been successfully formed.

---

## 2. Rationale

Every consensus round that produces a block must be recorded with its outcome and block reference. This CC closes the round journal entry for the PROPOSED path. It is the symmetric counterpart to CC_SKIP_ROUND_V0 for the round skip path.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_ASSEMBLE_RECORD_V0 | CT | Assemble round_record |
| 2 | CS_APPENDONLY_JSONL_V0 | CS | APPEND to CONSENSUS_ROUNDS |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_id | integer | true | Consensus round number |
| proposer_id | string | true | actor_id of the proposing validator |
| block_id | string | true | block_id produced by CC_FORM_BLOCK_V0 |
| timestamp | string | true | ISO 8601 timestamp of round completion |

---

## 5. Outputs

No outputs. This CC records state as a side effect only.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Round record appended to CONSENSUS_ROUNDS |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION on missing or invalid required inputs
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_RECORD_CONSENSUS_ROUND_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Record PROPOSED consensus round outcome to CONSENSUS_ROUNDS

  inputs:
    round_id:
      type: integer
      required: true
    proposer_id:
      type: string
      required: true
    block_id:
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
    - step: assemble_round_record
      transform: capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0
      inputs:
        fields:
          round_id: $.inputs.round_id
          proposer_id: $.inputs.proposer_id
          block_id: $.inputs.block_id
          outcome: PROPOSED
          timestamp: $.inputs.timestamp
      outputs:
        round_record: $.capability_result.record
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: append_round_record
        VIOLATION: exit

    - step: append_round_record
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: CONSENSUS_ROUNDS
      op: APPEND
      inputs:
        stream_id: $.inputs.round_id
        record: $.results.assemble_round_record.round_record
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: consensus_pos
  notes:
    - Only writes to CONSENSUS_ROUNDS (no CONSENSUS_EVENTS entry for PROPOSED path — event is in BLOCK_EVENTS via CC_FORM_BLOCK_V0)
    - Symmetric to CC_SKIP_ROUND_V0 for the propose path
```
