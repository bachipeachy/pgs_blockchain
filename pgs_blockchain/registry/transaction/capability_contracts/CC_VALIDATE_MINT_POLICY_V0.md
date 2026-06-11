# CC_VALIDATE_MINT_POLICY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_MINT_POLICY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Validate MINT transaction policy: to_wallet exists as a valid mint destination.

---

## 2. Rationale

Policy enforcement for MINT (SYSTEM authority):
- MINT is triggered by the protocol, not by an actor
- Confirms to_wallet exists in the WALLET store
- No ownership check required — SYSTEM transactions bypass actor authority

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ (to_wallet) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggered_by | string | true | Protocol event or system process that triggered this mint |
| to_wallet_id | string | true | Destination wallet to receive minted funds |
| amount | number | true | Mint amount in BACHI |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| to_wallet_record | object | Full to-wallet record |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | to_wallet found |
| NOT_FOUND | to_wallet does not exist |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_VALIDATE_MINT_POLICY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate MINT policy — destination wallet existence check (SYSTEM)

  inputs:
    triggered_by:
      type: string
      required: true
    to_wallet_id:
      type: string
      required: true
    amount:
      type: number
      required: true

  outputs:
    to_wallet_record:
      type: object

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: read_to_wallet
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: READ
      inputs:
        key: $.inputs.to_wallet_id
      outputs:
        to_wallet_record: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
