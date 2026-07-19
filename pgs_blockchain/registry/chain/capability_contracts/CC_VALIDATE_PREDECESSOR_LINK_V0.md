# CC_VALIDATE_PREDECESSOR_LINK_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_PREDECESSOR_LINK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_EXTRACT_PREDECESSOR_HASH_V0, CT_PURE_COMPARE_EQUAL_V0

---

## 1. Intent

CC_VALIDATE_PREDECESSOR_LINK_V0

---

## 2. Rationale



---

## 3. Pipeline

| Step | Capability | Type | Operation |
|---|---|---|---|
| s1 | CS_MUTABLE_JSON_V0 | CS | READ |
| s2 | CT_PURE_EXTRACT_PREDECESSOR_HASH_V0 | CT | COMPUTE |
| s3 | CT_PURE_COMPARE_EQUAL_V0 | CT | COMPUTE |

---

## 4. Inputs

(none)

---

## 5. Result Status Contract

Allowed outcomes: SUCCESS, VIOLATION

---

## Machine

```yaml
cc_code: CC_VALIDATE_PREDECESSOR_LINK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0
core:
  summary: CC_VALIDATE_PREDECESSOR_LINK_V0
  inputs: {}
  outputs:
    result_status:
      type: string
  result_status_contract:
    allowed:
    - SUCCESS
    - VIOLATION
    on_input_failure: VIOLATION
  pipeline:
  - step: s1
    side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
    store: chain_head
    op: READ
    inputs:
      key: head
    outputs:
      current_head: $.capability_result.value
    result_surface:
    - SUCCESS
    - VIOLATION
    on_result:
      SUCCESS: continue
      VIOLATION: exit
  - step: s2
    transform: blockchain::CT_PURE_EXTRACT_PREDECESSOR_HASH_V0
    op: COMPUTE
    inputs:
      block: $.inputs.proposed_block
    outputs:
      predecessor_hash: $.capability_result.predecessor_hash
    result_surface:
    - SUCCESS
    - VIOLATION
    on_result:
      SUCCESS: continue
      VIOLATION: exit
  - step: s3
    transform: capability_transforms::CT_PURE_COMPARE_EQUAL_V0
    op: COMPUTE
    inputs:
      left: $.results.s2.predecessor_hash
      right: $.results.s1.current_head
    outputs:
      is_match: $.capability_result.is_equal
    result_surface:
    - SUCCESS
    - VIOLATION
    on_result:
      SUCCESS: exit
      VIOLATION: exit
extensions:
  subdomain: chain
  notes: []
```
