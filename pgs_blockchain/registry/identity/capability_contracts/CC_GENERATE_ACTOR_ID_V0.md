# CC_GENERATE_ACTOR_ID_V0

## Header (Mandatory)

- **Artifact Code:** CC_GENERATE_ACTOR_ID_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0

---

## 1. Intent

Generate a deterministic actor ID from an actor record using content-addressable hashing.

---

## 2. Rationale

Actor IDs must be:
- Deterministic (same input always produces same ID)
- Collision-resistant
- Derived from actor data for auditability

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor data to hash for ID generation |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| actor_id | string | Deterministic actor identifier (AC-prefixed) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | ID generated successfully |
| VIOLATION | Invalid input format |

---

## 7. Failure Semantics

- Invalid actor_record format results in VIOLATION
- CT failure propagates as VIOLATION

---

## Machine

```yaml
cc_code: CC_GENERATE_ACTOR_ID_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Generate deterministic actor ID

  inputs:
    actor_record:
      type: object
      required: true

  outputs:
    actor_id:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_actor_id
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: AC
        data: $.inputs.actor_record
      outputs:
        actor_id: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```
