# IN_VALIDATOR_REGISTERED_V0

## Header (Mandatory)

- **Artifact Code:** IN_VALIDATOR_REGISTERED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** WF_REGISTER_VALIDATOR_V0

---

## 1. Intent

Register an existing actor as a validator node participant in the consensus layer.

---

## 2. Rationale

Validator registration is the entry point for consensus participation:
- Verifies the actor already exists in the identity registry before granting validator status
- Captures the validator's cryptographic identity (BLS12-381 pubkey) and stake declaration
- Records the registration event in the append-only validator lifecycle journal

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_REGISTER_VALIDATOR_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| validator_record | object | true | Proposed validator registration payload |
| validator_record.actor_id | string | true | PGS actor ID — primary key; must exist in the actor registry |
| validator_record.pubkey | string | true | BLS12-381 signing public key (hex-encoded, 0x-prefixed) |
| validator_record.withdrawal_credentials | string | true | Withdrawal destination credential (hex-encoded, 0x-prefixed) |
| validator_record.effective_balance | integer | true | Declared stake in BACHI — must be ≥ 32000000000 |
| validator_record.status | string | true | Initial lifecycle status — enum: ACTIVE_ONGOING, EXITED, SLASHED |
| validator_record.activation_epoch | integer | true | Epoch at which this validator became active |
| validator_record.exit_epoch | integer or null | true | Epoch at which this validator exits; null if not scheduled |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Payload admitted — all required fields present, pubkey format valid, effective_balance meets minimum |
| NACK | Payload rejected — missing required fields, invalid pubkey format, or effective_balance below minimum |

---

## 6. Domain

- **Domain:** pgs.consensus_pos.validator
- **Notes:**
  - Actor must already be registered in the identity registry (enforced by CC_CHECK_ACTOR_EXISTS_V0)
  - One actor maps to at most one validator record (enforced by CC_CHECK_VALIDATOR_EXISTS_V0 duplicate gate)
  - effective_balance minimum is 32000000000
  - status, activation_epoch, and exit_epoch are canonical lifecycle fields required for CC_QUERY_ELIGIBLE_VALIDATORS_V0 eligibility filtering (status=ACTIVE_ONGOING AND effective_balance present)

---

## Machine

```yaml
in_code: IN_VALIDATOR_REGISTERED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Register an existing actor as a validator node
  workflow: WF_REGISTER_VALIDATOR_V0

  inputs:
    validator_record:
      type: object
      required: true
      description: Proposed validator registration payload
      fields:
        actor_id:
          type: string
          required: true
        pubkey:
          type: string
          required: true
          format: hex
          prefix: "0x"
        withdrawal_credentials:
          type: string
          required: true
          format: hex
          prefix: "0x"
        effective_balance:
          type: integer
          required: true
          minimum: 32000000000
        status:
          type: string
          required: true
          enum: [ACTIVE_ONGOING, EXITED, SLASHED]
          description: Initial lifecycle status
        activation_epoch:
          type: integer
          required: true
          description: Epoch at which this validator became active
        exit_epoch:
          type: [integer, "null"]
          required: true
          description: Epoch at which this validator exits; null if not scheduled

  outcomes:
    ACK:
      description: Payload admitted — all required fields present, pubkey format valid, effective_balance meets minimum
    NACK:
      description: Payload rejected — missing required fields, invalid pubkey format, or effective_balance below minimum

extensions:
  domain: pgs.consensus_pos.validator
  notes:
    - Actor must already be registered in the identity registry (enforced by CC_CHECK_ACTOR_EXISTS_V0)
    - One actor maps to at most one validator record (enforced by CC_CHECK_VALIDATOR_EXISTS_V0 + CC_WRITE_VALIDATOR_RECORD_V0)
    - effective_balance minimum is 32000000000 Gwei (32 ETH)
```
