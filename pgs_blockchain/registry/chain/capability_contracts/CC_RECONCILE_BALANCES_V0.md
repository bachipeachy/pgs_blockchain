# CC_RECONCILE_BALANCES_V0

## Header (Mandatory)

- **Artifact Code:** CC_RECONCILE_BALANCES_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0, CT_PURE_DERIVE_BALANCES_V0

---

## 1. Intent

CC_RECONCILE_BALANCES_V0

---

## 2. Rationale



---

## 3. Pipeline

| Step | Capability | Type | Operation |
|---|---|---|---|
| s1 | CS_APPENDONLY_JSONL_V0 | CS | GET_ALL |
| s2 | CT_PURE_DERIVE_BALANCES_V0 | CT | COMPUTE |

---

## 4. Inputs

(none)

---

## 5. Result Status Contract

Allowed outcomes: SUCCESS

---

## Machine

```yaml
cc_code: CC_RECONCILE_BALANCES_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0
core:
  summary: CC_RECONCILE_BALANCES_V0
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
    side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
    store: chain
    op: GET_ALL
    inputs: {}
    outputs:
      committed_history: $.capability_result.entries
    result_surface:
    - SUCCESS
    on_result:
      SUCCESS: continue
  - step: s2
    transform: blockchain::CT_PURE_DERIVE_BALANCES_V0
    op: COMPUTE
    inputs:
      committed_history: $.results.s1.committed_history
    outputs:
      reconciled_balances: $.capability_result.reconciled_balances
    result_surface:
    - SUCCESS
    on_result:
      SUCCESS: exit
extensions:
  subdomain: chain
  notes: []
```
