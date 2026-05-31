# CC_CHECK_ACTOR_EXISTS_V0

## Header (Mandatory)

- **Artifact Code:** CC_CHECK_ACTOR_EXISTS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0

---

## 1. Intent

Verify that an actor_id exists in the actor registry. Used as the actor prerequisite gate by
subdomains that require actor existence before granting domain authority.

---

## 2. Rationale

Actor existence must be verifiable without resolving KYC attributes. Existing capabilities
(CC_RESOLVE_ACTOR_ID_V0) resolve actor_id from KYC data — wrong shape for a check-by-actor_id
gate. CS_REGISTRY_V0 provides an EXISTS operation against any registered store; this CC wraps
it for the actor store specifically.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | RESOLVE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Actor ID to verify against the actor registry |

---

## 5. Outputs

No outputs. This CC answers existence only; downstream CCs receive actor_id from the original payload.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | actor_id exists in the actor registry |
| NOT_FOUND | actor_id not present in the actor registry |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- NOT_FOUND is a terminal failure for any workflow that requires actor prerequisite
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_CHECK_ACTOR_EXISTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Verify actor exists in the actor registry

  inputs:
    actor_id:
      type: string
      required: true

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_actor_exists
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: ACTOR
      op: RESOLVE
      inputs:
        key_or_address: $.inputs.actor_id
      outputs: {}
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
