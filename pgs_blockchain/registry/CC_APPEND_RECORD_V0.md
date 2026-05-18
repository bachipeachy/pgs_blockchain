# CC_APPEND_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CC_APPEND_RECORD_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Append a record to an append-only log with actor attribution and optional stream partitioning.

---

## 2. Rationale

Generic append capability enables:
- Immutable audit/event logs
- Preserved write order
- Actor attribution for audit
- Logical partitioning via stream_id

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| record | object | true | Record to append (will be timestamped automatically) |
| stream_id | string | false | Optional stream identifier for logical partitioning |
| actor_id | string | true | Actor performing the append (enables audit trail) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| record_id | string | Unique ID of appended record |
| sequence_number | integer | Sequential position in the log |
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Record appended successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR
- APPEND is not idempotent; retries create duplicate records

---

## 8. Guarantees

- Immutable append-only semantics
- Preserved write order
- Server-side timestamp attribution
- Actor attribution audit

---

## Machine

```yaml
cc_code: CC_APPEND_RECORD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Append a record to an append-only log
  description: Immutably append a record to the audit/event log with timestamp and actor attribution

  inputs:
    record:
      type: object
      required: true
      description: Record to append to log (will be timestamped automatically)
    stream_id:
      type: string
      required: false
      description: Optional stream identifier for logical partitioning
    actor_id:
      type: string
      required: true
      description: Actor performing the append (enables audit trail)

  outputs:
    record_id:
      type: string
      required: true
      description: Unique ID of appended record
    sequence_number:
      type: integer
      required: false
      description: Sequential position in the log
    result_status:
      type: string
      required: true
      description: Normalized result of append operation

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: append_record
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      op: APPEND
      inputs:
        record: $.inputs.record
        stream_id: $.inputs.stream_id
        actor_id: $.inputs.actor_id
      outputs:
        record_id: $.capability_result.record_id
        sequence_number: $.capability_result.sequence_number
        result_status: $.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  idempotency:
    safe_to_retry: false
    note: APPEND is not idempotent; retries will create duplicate records

  guarantees:
    - Immutable append-only semantics
    - Preserved write order
    - Server-side timestamp attribution
    - Actor attribution audit

  notes:
    - Append-only log provides auditability and event sourcing
    - No deduplication is performed
    - stream_id allows logical partitioning without separate files
```
