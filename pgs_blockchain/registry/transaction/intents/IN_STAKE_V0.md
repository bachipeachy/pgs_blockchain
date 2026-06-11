# IN_STAKE_V0

## Header (Mandatory)

- **Artifact Code:** IN_STAKE_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_STAKE_V0

---

## 1. Intent

Submit a STAKE transaction — move BACHI from an actor wallet into the staking pool.

---

## 2. Rationale

STAKE is an ENDUSER operation. The actor stakes from their own wallet.
The destination (POOL wallet) is auto-resolved by the policy CC — not supplied by the caller.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_STAKE_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor record for identity resolution |
| actor_record.email_registration | string | true | Actor email (format: email) |
| from_wallet_id | string | true | Source wallet identifier |
| amount | number | true | Stake amount in BACHI |
| gas_limit | integer | false | Gas limit (default 21000) |
| max_fee_per_gas | string | false | Max fee per gas in wei (default "20000000000") |
| max_priority_fee_per_gas | string | false | Max priority fee per gas in wei (default "1000000000") |
| memo | string | false | Optional transaction memo |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Stake intent accepted |
| NACK | Stake intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** ENDUSER
- **Note:** to_address auto-resolved to POOL wallet by CC_VALIDATE_STAKE_POLICY_V0

---

## Machine

```yaml
in_code: IN_STAKE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit STAKE transaction (ENDUSER)
  workflow: WF_STAKE_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Actor record for identity resolution
      fields:
        email_registration:
          type: string
          required: true
          format: email
    from_wallet_id:
      type: string
      required: true
      description: Source wallet identifier
    amount:
      type: number
      required: true
      description: Stake amount in BACHI
    gas_limit:
      type: integer
      default: 21000
      description: Gas limit
    max_fee_per_gas:
      type: string
      default: "20000000000"
      description: Max fee per gas in wei
    max_priority_fee_per_gas:
      type: string
      default: "1000000000"
      description: Max priority fee per gas in wei
    memo:
      type: string
      required: false
      description: Optional transaction memo

  outcomes:
    ACK:
      description: Stake intent accepted
    NACK:
      description: Stake intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: ENDUSER
```
