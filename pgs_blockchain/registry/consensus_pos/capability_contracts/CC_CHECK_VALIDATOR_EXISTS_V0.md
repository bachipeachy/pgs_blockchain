# CC_CHECK_VALIDATOR_EXISTS_V0

## Header (Mandatory)

- **Artifact Code:** CC_CHECK_VALIDATOR_EXISTS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Check if an actor is already registered as a validator — gates the write step to prevent duplicate registration.

---

## 2. Rationale

Duplicate detection for the VALIDATOR store:
- VALIDATOR store uses CS_MUTABLE_JSON_V0 (mutable JSON, STRUCTURE-resolved path)
- CS_MUTABLE_JSON_V0 GET returns NOT_FOUND when the key is absent, enabling direct workflow routing
- NOT_FOUND is the happy path — actor is new to the validator set, proceed to write
- SUCCESS means the actor is already registered — abort, duplicate request

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ |

Uses READ (not EXISTS) because the execution engine routes on `result_status`. READ returns `NOT_FOUND`
when the key is absent, enabling direct workflow routing. EXISTS always returns `SUCCESS` with a
boolean, which the engine cannot branch on.

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Actor ID to check for existing validator registration |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | NOT_FOUND (new) or SUCCESS (already registered) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| NOT_FOUND | Actor not yet registered as validator — proceed to write |
| SUCCESS | Actor already registered as validator — abort, duplicate |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- NOT_FOUND is the expected happy path — actor is new to the validator set
- SUCCESS means already registered — duplicate; workflow exits without writing
- Invalid actor_id results in VIOLATION
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_CHECK_VALIDATOR_EXISTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Check if actor already has a validator record in the VALIDATOR store

  inputs:
    actor_id:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [NOT_FOUND, SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_validator_exists
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: VALIDATOR
      op: READ
      inputs:
        key: $.inputs.actor_id
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
