# CC_CREATE_WALLET_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CC_CREATE_WALLET_RECORD_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CS_REGISTRY_V0

---

## 1. Intent

Assemble a complete V0 wallet record from upstream CC outputs and payload data, persist the full record to CS_MUTABLE_JSON_V0, then register a pointer in CS_REGISTRY_V0.

---

## 2. Rationale

Wallet record creation:
- Composes the full wallet record from crypto-derived fields (CC_DERIVE_WALLET_KEYS_V0) and payload fields
- Persists via registry with stable addressing
- Immutable binding once created
- Record structure matches V0 canonical schema

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |
| 2 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| wallet_id | string | true | CC_GENERATE_WALLET_ID_V0 | Wallet identifier (WAL-prefixed) |
| actor_id | string | true | CC_RESOLVE_ACTOR_ID_V0 | Owner actor identifier |
| wallet_type | string | true | payload | Wallet type — enum: STANDARD, STAKING, MINT, BURN, POOL |
| address | string | true | CC_GENERATE_WALLET_ID_V0 | Deterministic wallet address (0x-prefixed, 40 hex chars) |
| currency | string | false | payload | Currency code (default: BACHI) |

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
| SUCCESS | Wallet registered successfully |
| ALREADY_EXISTS | Wallet already exists |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Duplicate wallet results in ALREADY_EXISTS
- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_CREATE_WALLET_RECORD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Assemble and persist V0 wallet record

  inputs:
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    wallet_type:
      type: string
      required: true
      enum: [STANDARD, STAKING, MINT, BURN, POOL]
    address:
      type: string
      required: true
      description: Deterministic wallet address (0x-prefixed, 40 hex chars)
    currency:
      type: string
      required: false
      default: BACHI

  outputs:
    result_status:
      type: string
    address:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: write_wallet_state
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: WRITE
      inputs:
        key: $.inputs.wallet_id
        value:
          wallet_id: $.inputs.wallet_id
          actor_id: $.inputs.actor_id
          wallet_type: $.inputs.wallet_type
          address: $.inputs.address
          balance: 0
          currency: $.inputs.currency
          status: ACTIVE
          created_at: "{{timestamp}}"
          last_modified: "{{timestamp}}"
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: register_wallet_index
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.inputs.wallet_id
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.wallet_id
      outputs:
        result_status: $.capability_result.result_status
        address: $.capability_result.address
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
