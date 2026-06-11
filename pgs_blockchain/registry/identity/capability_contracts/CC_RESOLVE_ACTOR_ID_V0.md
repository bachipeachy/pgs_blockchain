# CC_RESOLVE_ACTOR_ID_V0

## Header (Mandatory)

- **Artifact Code:** CC_RESOLVE_ACTOR_ID_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0

---

## 1. Intent

Resolve an actor ID from KYC attributes by looking up the alias index.

---

## 2. Rationale

Actor resolution by KYC enables:
- Finding existing actors by their identifying attributes
- Preventing duplicate actor registration
- Supporting idempotent workflows

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |
| 2 | CS_REGISTRY_V0 | CS | RESOLVE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor data for KYC key generation |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| actor_id | string | Resolved actor identifier |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Actor ID resolved successfully |
| NOT_FOUND | KYC key not registered |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- CT failure results in VIOLATION and exit
- Unknown KYC key results in NOT_FOUND
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_RESOLVE_ACTOR_ID_V0
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Resolve actor ID from KYC key

  inputs:
    actor_record:
      type: object
      required: true

  outputs:
    actor_id:
      type: string

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_kyc_key
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: A_KEY
        data:
          first_name: $.inputs.actor_record.first_name
          last_name: $.inputs.actor_record.last_name
          email: $.inputs.actor_record.email_registration
      outputs:
        kyc_key: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: resolve_actor_from_kyc
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: ACTOR
      op: RESOLVE
      inputs:
        key_or_address: $.results.generate_kyc_key.kyc_key
      outputs:
        actor_id: $.capability_result.target_ref
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
