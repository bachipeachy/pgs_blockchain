# CC_WRITE_VALIDATOR_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CC_WRITE_VALIDATOR_RECORD_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Write the validator record to the VALIDATOR store, keyed by actor_id.

---

## 2. Rationale

Validator record persistence:
- VALIDATOR store uses CS_MUTABLE_JSON_V0 (mutable JSON, STRUCTURE-resolved path)
- PUT is idempotent — last-write-wins semantics apply, but execution only reaches this step after
  CC_CHECK_VALIDATOR_EXISTS_V0 confirms NOT_FOUND, so no overwrite occurs in normal flow
- actor_id is the sole primary key — no secondary key generation needed

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| validator_record | object | true | Full validator registration payload keyed by actor_id |
| validator_record.actor_id | string | true | PGS actor ID — store key |
| validator_record.pubkey | string | true | BLS12-381 signing public key (hex, 0x-prefixed) |
| validator_record.withdrawal_credentials | string | true | Withdrawal credential (hex, 0x-prefixed) |
| validator_record.effective_balance | integer | true | Declared stake in Gwei (≥ 32000000000) |
| validator_record.balance | integer | true | Current balance in Gwei (initial = effective_balance) |
| validator_record.slashed | boolean | true | Whether validator has been slashed (initial: false) |
| validator_record.status | string | true | Validator lifecycle status (initial: PENDING_INITIALIZED) |
| validator_record.activation_eligibility_epoch | integer | false | Epoch when eligible for activation (null until set) |
| validator_record.activation_epoch | integer | false | Epoch when activated (null until set) |
| validator_record.exit_epoch | integer | false | Epoch when exited (null until set) |
| validator_record.withdrawable_epoch | integer | false | Epoch when withdrawable (null until set) |
| validator_record.registered_at | string | true | ISO 8601 timestamp of registration |

---

## 5. Outputs

No outputs. This CC writes to the store as a side effect; it does not return data to the caller.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Validator record written successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- BACKEND_ERROR propagates as a hard failure
- VIOLATION on invalid input format

---

## Machine

```yaml
cc_code: CC_WRITE_VALIDATOR_RECORD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Write the validator record to the VALIDATOR store keyed by actor_id

  inputs:
    validator_record:
      type: object
      required: true
      fields:
        actor_id:
          type: string
          required: true
        pubkey:
          type: string
          required: true
        withdrawal_credentials:
          type: string
          required: true
        effective_balance:
          type: integer
          required: true
          minimum: 32000000000
        balance:
          type: integer
          required: true
        slashed:
          type: boolean
          required: true
        status:
          type: string
          required: true
          enum: [PENDING_INITIALIZED, PENDING_QUEUED, ACTIVE_ONGOING, ACTIVE_EXITING, ACTIVE_SLASHED, EXITED_UNSLASHED, EXITED_SLASHED, WITHDRAWAL_POSSIBLE, WITHDRAWAL_DONE]
        activation_eligibility_epoch:
          type: integer
          required: false
        activation_epoch:
          type: integer
          required: false
        exit_epoch:
          type: integer
          required: false
        withdrawable_epoch:
          type: integer
          required: false
        registered_at:
          type: string
          required: true
          format: date-time

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: write_validator_record
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: VALIDATOR
      op: WRITE
      inputs:
        key: $.inputs.validator_record.actor_id
        value: $.inputs.validator_record
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
