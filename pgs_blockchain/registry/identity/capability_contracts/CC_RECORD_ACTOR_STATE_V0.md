# CC_RECORD_ACTOR_STATE_V0

## Header (Mandatory)

- **Artifact Code:** CC_RECORD_ACTOR_STATE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Record an actor state transition to the actor state log.

---

## 2. Rationale

Actor state transitions require:
- Immutable audit trail
- Timestamped state changes
- Support for state machine reconstruction

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Actor identifier |
| old_state | string | false | Previous state (optional for initial) |
| new_state | string | true | New state |
| reason | string | false | Reason for transition |
| timestamp | string | true | ISO-8601 timestamp |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | State recorded successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR
- APPEND is not idempotent; retries create duplicates

---

## Machine

```yaml
cc_code: CC_RECORD_ACTOR_STATE_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Record actor state transition

  inputs:
    actor_id:
      type: string
      required: true
    old_state:
      type: string
      required: false
    new_state:
      type: string
      required: true
    reason:
      type: string
      required: false
    timestamp:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: record_state_transition
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: ACTOR_EVENTS
      op: APPEND
      inputs:
        stream_id: $.inputs.actor_id
        actor_id: $.inputs.actor_id
        record:
          actor_id: $.inputs.actor_id
          old_state: $.inputs.old_state
          new_state: $.inputs.new_state
          reason: $.inputs.reason
          timestamp: $.inputs.timestamp
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
