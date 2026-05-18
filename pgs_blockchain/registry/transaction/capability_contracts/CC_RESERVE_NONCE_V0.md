# CC_RESERVE_NONCE_V0

## Header (Mandatory)

- **Artifact Code:** CC_RESERVE_NONCE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_INCREMENT_WALLET_NONCE_V0, CS_MUTABLE_JSON_V0

---

## 1. Intent

Reserve the current nonce and write the incremented value back to wallet state.

---

## 2. Rationale

The wallet record (including current nonce) is read by CC_VALIDATE_TX_POLICY_V0
and passed through the payload. This CC increments the nonce, writes the updated
record back, and outputs the reserved nonce for transaction building.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_INCREMENT_WALLET_NONCE_V0 | CT | INCREMENT_WALLET_NONCE |
| 2 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| wallet_id | string | true | Wallet to update nonce for |
| wallet_record | object | true | Current wallet record from CC_VALIDATE_TX_POLICY_V0 |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| nonce | integer | Reserved nonce value for this transaction |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Nonce reserved and state updated |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage write failure |

---

## Machine

```yaml
cc_code: CC_RESERVE_NONCE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Reserve nonce and write incremented value to wallet state

  inputs:
    wallet_id:
      type: string
      required: true
    wallet_record:
      type: object
      required: true

  outputs:
    nonce:
      type: integer

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]

  pipeline:
    - step: increment_wallet_nonce
      transform: blockchain::CT_PURE_INCREMENT_WALLET_NONCE_V0
      op: INCREMENT_WALLET_NONCE
      inputs:
        wallet_record: $.inputs.wallet_record
      outputs:
        updated_wallet_record: $.capability_result.updated_wallet_record
        nonce: $.capability_result.nonce
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: write_updated_wallet
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: WRITE
      inputs:
        key: $.inputs.wallet_id
        value: $.results.increment_wallet_nonce.updated_wallet_record
      outputs:
        nonce: $.results.increment_wallet_nonce.nonce
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

  error_codes:
    BACKEND_ERROR: TX_NONCE_CONFLICT
```
