# CC_PERSIST_VERIFIED_ACTOR_V0

## Header (Mandatory)

- **Artifact Code:** CC_PERSIST_VERIFIED_ACTOR_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0

---

## 1. Intent

Persist a verified actor record by registering it in the verified actor index.

---

## 2. Rationale

Verified actors need:
- Persistent storage reference
- Stable addressing via registry
- Immutable binding once verified

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Actor identifier to register |
| target_cs | string | true | Target storage capability |
| target_ref | string | true | Reference within target storage |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |
| address | string | Registry address assigned |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Actor registered successfully |
| ALREADY_EXISTS | Actor already in verified index |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Duplicate registration results in ALREADY_EXISTS
- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_PERSIST_VERIFIED_ACTOR_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Persist verified actor record

  inputs:
    actor_id:
      type: string
      required: true
    target_cs:
      type: string
      required: true
    target_ref:
      type: string
      required: true

  outputs:
    result_status:
      type: string
    address:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR, ALREADY_EXISTS]
    on_input_failure: VIOLATION

  pipeline:
    - step: register_verified_actor
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: ACTOR
      op: REGISTER
      inputs:
        key: $.inputs.actor_id
        target_cs: $.inputs.target_cs
        target_ref: $.inputs.target_ref
      outputs:
        result_status: $.capability_result.result_status
        address: $.capability_result.address
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
        ALREADY_EXISTS: exit
```
