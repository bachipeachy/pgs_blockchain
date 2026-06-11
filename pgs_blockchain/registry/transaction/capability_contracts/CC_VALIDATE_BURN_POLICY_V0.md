# CC_VALIDATE_BURN_POLICY_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_BURN_POLICY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Validate BURN transaction policy: from_wallet exists as a valid burn source.

---

## 2. Rationale

Policy enforcement for BURN (SYSTEM authority):
- BURN is triggered by the protocol, not by an actor
- Confirms from_wallet exists in the WALLET store
- No ownership check required — SYSTEM transactions bypass actor authority

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ (from_wallet) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggered_by | string | true | Protocol event or system process that triggered this burn |
| from_wallet_id | string | true | Source wallet from which funds are burned |
| amount | number | true | Burn amount in BACHI |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| from_wallet_record | object | Full from-wallet record |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | from_wallet found |
| NOT_FOUND | from_wallet does not exist |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## Machine

```yaml
cc_code: CC_VALIDATE_BURN_POLICY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate BURN policy — source wallet existence check (SYSTEM)

  inputs:
    triggered_by:
      type: string
      required: true
    from_wallet_id:
      type: string
      required: true
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
