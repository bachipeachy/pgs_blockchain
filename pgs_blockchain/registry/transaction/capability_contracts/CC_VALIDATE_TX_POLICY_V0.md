# CC_VALIDATE_TX_POLICY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_TX_POLICY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_REGISTRY_V0, CS_MUTABLE_JSON_V0, CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0

---

## 1. Intent

Validate transaction policy: wallet ownership, EOA capability, and value limits.

---

## 2. Rationale

Policy validation ensures:
- Wallet exists and belongs to the submitting actor
- Wallet supports EOA transactions
- Value does not exceed protocol limits (unlimited in V0)

Balance validation is deferred to the consensus module.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_REGISTRY_V0 | CS | RESOLVE |
| 2 | CS_MUTABLE_JSON_V0 | CS | READ |
| 3 | CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0 | CT | EXTRACT_WALLET_TX_FIELDS |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| wallet_id | string | true | Wallet to validate |
| actor_id | string | true | Actor submitting the transaction |
| value | string | true | Transfer value in wei |
| tx_type | string | true | Transaction type (ETH) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| from_address | string | EOA address from wallet record |
| wallet_record | object | Full wallet record for downstream use |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Wallet exists, owned by actor, supports EOA |
| NOT_FOUND | Wallet not found in index |
| VIOLATION | Ownership mismatch or EOA not supported (TX_POLICY_VIOLATION) |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_VALIDATE_TX_POLICY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate transaction policy — ownership, capability, limits

  inputs:
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    value:
      type: string
      required: true
    tx_type:
      type: string
      required: true

  outputs:
    from_address:
      type: string
    current_nonce:
      type: integer
    wallet_record:
      type: object

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: resolve_wallet_registry
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: RESOLVE
      inputs:
        key_or_address: $.inputs.wallet_id
      outputs:
        wallet_ref: $.capability_result.target_ref
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: read_wallet_record
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: READ
      inputs:
        key: $.inputs.wallet_id
      outputs:
        wallet_data: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: extract_wallet_tx_fields
      transform: blockchain::CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
      op: EXTRACT_WALLET_TX_FIELDS
      inputs:
        wallet_record: $.results.read_wallet_record.wallet_data
      outputs:
        from_address: $.capability_result.from_address
        current_nonce: $.capability_result.current_nonce
        wallet_record: $.results.read_wallet_record.capability_result.value
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

  error_codes:
    VIOLATION: TX_POLICY_VIOLATION
```
