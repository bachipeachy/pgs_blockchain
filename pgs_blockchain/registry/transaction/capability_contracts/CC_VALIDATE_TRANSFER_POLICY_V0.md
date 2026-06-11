# CC_VALIDATE_TRANSFER_POLICY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_TRANSFER_POLICY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Validate TRANSFER transaction policy: from_wallet exists and is owned by the submitting actor.

---

## 2. Rationale

Policy enforcement for TRANSFER:
- Confirms from_wallet exists in the WALLET store
- Confirms from_wallet.actor_id matches the submitting actor
- Returns the wallet record for downstream CC use (balance check deferred to consensus)

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ (from_wallet) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Submitting actor ID |
| from_wallet_id | string | true | Source wallet to validate |
| to_wallet_id | string | false | Destination wallet (may be external address) |
| amount | number | true | Transfer amount in BACHI |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| from_wallet_record | object | Full from-wallet record |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | from_wallet found and owned by actor |
| NOT_FOUND | from_wallet does not exist |
| VIOLATION | from_wallet.actor_id does not match actor_id |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_VALIDATE_TRANSFER_POLICY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate TRANSFER policy — wallet ownership check

  inputs:
    actor_id:
      type: string
      required: true
    from_wallet_id:
      type: string
      required: true
    to_wallet_id:
      type: string
      required: false
    amount:
      type: number
      required: true

  outputs:
    from_wallet_record:
      type: object

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: read_from_wallet
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: READ
      inputs:
        key: $.inputs.from_wallet_id
      outputs:
        from_wallet_record: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
