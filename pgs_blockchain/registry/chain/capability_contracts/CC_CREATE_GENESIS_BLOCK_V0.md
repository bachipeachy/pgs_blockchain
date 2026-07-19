# CC_CREATE_GENESIS_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CC_CREATE_GENESIS_BLOCK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_HASH_BLOCK_V0, CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0

---

## 1. Intent

CC_CREATE_GENESIS_BLOCK_V0

---

## 2. Rationale



---

## 3. Pipeline

| Step | Capability | Type | Operation |
|---|---|---|---|
| s1 | CT_PURE_HASH_BLOCK_V0 | CT | COMPUTE |
| s2 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |
| s3 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

(none)

---

## 5. Result Status Contract

Allowed outcomes: SUCCESS

---

## Machine

```yaml
cc_code: CC_CREATE_GENESIS_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0
core:
  summary: CC_CREATE_GENESIS_BLOCK_V0
  inputs: {}
  outputs:
    result_status:
      type: string
  result_status_contract:
    allowed:
    - SUCCESS
    on_input_failure: VIOLATION
  pipeline:
  - step: s1
    transform: blockchain::CT_PURE_HASH_BLOCK_V0
    op: COMPUTE
    inputs:
      block: $.inputs.genesis_block_content
    outputs:
      content_hash: $.capability_result.content_hash
    result_surface:
    - SUCCESS
    on_result:
      SUCCESS: continue
  - step: s2
    side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
    store: chain
    op: APPEND
    inputs:
      record: $.inputs.genesis_block_content
    outputs:
      genesis_block: $.capability_result.record_id
    result_surface:
    - SUCCESS
    on_result:
      SUCCESS: continue
  - step: s3
    side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
    store: chain_head
    op: WRITE
    inputs:
      key: head
      value: $.results.s1.content_hash
    outputs: {}
    result_surface:
    - SUCCESS
    on_result:
      SUCCESS: exit
extensions:
  subdomain: chain
  notes: []
```
