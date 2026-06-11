# CC_VALIDATE_POOL_POLICY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_POOL_POLICY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Validate POOL transaction policy: the system POOL wallet exists and is reachable.

---

## 2. Rationale

Policy enforcement for POOL (SYSTEM authority):
- POOL transactions redistribute collected fees into the protocol pool
- Validates the POOL wallet exists in the WALLET store
- No actor ownership check — SYSTEM authority only

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ (pool_wallet) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggered_by | string | true | Protocol event or system process that triggered this pool operation |
| pool_wallet_id | string | true | POOL system wallet identifier |
| amount | number | true | Pool amount in BACHI |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| pool_wallet_record | object | Full pool-wallet record |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | pool_wallet found |
| NOT_FOUND | pool_wallet does not exist |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_VALIDATE_POOL_POLICY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate POOL policy — pool wallet existence check (SYSTEM)

  inputs:
    triggered_by:
      type: string
      required: true
    pool_wallet_id:
      type: string
      required: true
    amount:
      type: number
      required: true

  outputs:
    pool_wallet_record:
      type: object

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: read_pool_wallet
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: READ
      inputs:
        key: $.inputs.pool_wallet_id
      outputs:
        pool_wallet_record: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
