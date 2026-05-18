# CC_REGISTER_ACTOR_KYC_V0

## Header (Mandatory)

- **Artifact Code:** CC_REGISTER_ACTOR_KYC_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0

---

## 1. Intent

Register an actor's KYC key to actor ID mapping in the alias index.

---

## 2. Rationale

KYC-based lookup requires:
- Deterministic KYC key generation from actor data
- Registry binding from KYC key to actor ID
- Support for actor resolution by KYC attributes

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |
| 2 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor data for KYC key generation |
| actor_id | string | true | Actor ID to bind to KYC key |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| address | string | Registry address assigned |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | KYC key registered successfully |
| ALREADY_EXISTS | KYC key already registered |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- CT failure results in VIOLATION and exit
- Duplicate KYC key continues (idempotent for re-registration)
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_REGISTER_ACTOR_KYC_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Register actor KYC key to ID mapping

  inputs:
    actor_record:
      type: object
      required: true
    actor_id:
      type: string
      required: true

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_kyc_key
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: KYC
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

    - step: register_kyc_mapping
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: ACTOR
      op: REGISTER
      inputs:
        key: $.results.generate_kyc_key.kyc_key
        target_cs: CS_APPENDONLY_JSONL_V0
        target_ref: $.inputs.actor_id
        stream_id: $.inputs.actor_id
      outputs: {}
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
