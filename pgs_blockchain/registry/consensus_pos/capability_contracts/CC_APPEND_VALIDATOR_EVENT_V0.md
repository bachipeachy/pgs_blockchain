# CC_APPEND_VALIDATOR_EVENT_V0

## Header (Mandatory)

- **Artifact Code:** CC_APPEND_VALIDATOR_EVENT_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Append a validator lifecycle event to the append-only validator event journal.

---

## 2. Rationale

Validator lifecycle events require:
- Immutable append-only event log (no deletion, no mutation)
- Event sourcing capability for audit and observability
- Audit trail across all validator lifecycle transitions

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| event_type | string | true | Event type code |
| actor_id | string | true | PGS actor ID of the validator |
| data | object | true | Event payload data |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Event appended successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR
- APPEND is not idempotent; retries create duplicate events

---

## Machine

```yaml
cc_code: CC_APPEND_VALIDATOR_EVENT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Append a validator lifecycle event to the append-only event journal

  inputs:
    event_type:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    data:
      type: object
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: append_validator_event
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: VALIDATOR_EVENTS
      op: APPEND
      inputs:
        stream_id: $.inputs.actor_id
        actor_id: $.inputs.actor_id
        record:
          event_code: $.inputs.event_type
          actor_id: $.inputs.actor_id
          payload: $.inputs.data
          timestamp: "2025-01-01T00:00:00Z"
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  description: Appends an event to the validator lifecycle event journal
```
