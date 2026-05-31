# CC_WRITE_VALIDATOR_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CC_WRITE_VALIDATOR_RECORD_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Write the validator record to the VALIDATOR store, keyed by actor_id.

---

## 2. Rationale

Validator record persistence:
- VALIDATOR store uses CS_MUTABLE_JSON_V0 (mutable JSON, STRUCTURE-resolved path)
- PUT is idempotent — last-write-wins semantics apply, but execution only reaches this step after
  CC_CHECK_VALIDATOR_EXISTS_V0 confirms NOT_FOUND, so no overwrite occurs in normal flow
- actor_id is the sole primary key — no secondary key generation needed

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| validator_record | object | true | Full validator registration payload keyed by actor_id |

---

## 5. Outputs

No outputs. This CC writes to the store as a side effect; it does not return data to the caller.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Validator record written successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- BACKEND_ERROR propagates as a hard failure
- VIOLATION on invalid input format

---

## Machine

```yaml
cc_code: CC_WRITE_VALIDATOR_RECORD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Write the validator record to the VALIDATOR store keyed by actor_id

  inputs:
    validator_record:
      type: object
      required: true

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: write_validator_record
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: VALIDATOR
      op: WRITE
      inputs:
        key: $.inputs.validator_record.actor_id
        value: $.inputs.validator_record
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
