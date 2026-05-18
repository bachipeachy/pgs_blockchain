# CC_CHECK_WALLET_EXISTS_V0

## Header (Mandatory)

- **Artifact Code:** CC_CHECK_WALLET_EXISTS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0

---

## 1. Intent

Check if a wallet ID already exists in the registry before proceeding with key derivation.

---

## 2. Rationale

Wallet existence gate:
- Prevents duplicate wallet creation
- Gates crypto derivation pipeline — avoids unnecessary entropy generation for duplicate requests
- Pure read operation, idempotent

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | RESOLVE |

Uses RESOLVE (not EXISTS) because the execution engine routes on `result_status`. RESOLVE returns `NOT_FOUND` when the key is absent, enabling direct workflow routing. EXISTS always returns `SUCCESS` with a boolean, which the engine cannot branch on.

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| wallet_id | string | true | Wallet identifier to check |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | NOT_FOUND (new) or SUCCESS (exists) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| NOT_FOUND | Wallet does not exist — gate passes, proceed to derivation |
| SUCCESS | Wallet already exists — abort, duplicate request |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Registry unavailable |

---

## 7. Failure Semantics

- NOT_FOUND is the expected happy path — wallet is new, proceed
- SUCCESS means the wallet already exists and creation should stop
- Invalid wallet_id results in VIOLATION
- Registry unavailable results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_CHECK_WALLET_EXISTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Check wallet existence in registry

  inputs:
    wallet_id:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [NOT_FOUND, SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: check_wallet_exists
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: WALLET
      op: RESOLVE
      inputs:
        key_or_address: $.inputs.wallet_id
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
