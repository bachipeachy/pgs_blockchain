# IN_REWARD_V0

## Header (Mandatory)

- **Artifact Code:** IN_REWARD_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_REWARD_V0

---

## 1. Intent

Submit a REWARD transaction — distribute staking reward from the POOL wallet to a validator's wallet.

---

## 2. Rationale

REWARD is a SYSTEM operation triggered by block finalization.
The source (POOL wallet) is auto-resolved. The destination wallet and block reference are declared.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_REWARD_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| to_wallet_id | string | true | Destination wallet identifier (validator's wallet) |
| amount | number | true | Reward amount in BACHI |
| block_hash | string | true | Block hash that triggered this reward |
| triggered_by | string | true | System trigger reference |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Reward intent accepted |
| NACK | Reward intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** SYSTEM
- **Note:** from_address auto-resolved to POOL wallet; no actor_record; no gas params

---

## Machine

```yaml
in_code: IN_REWARD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit REWARD transaction (SYSTEM)
  workflow: WF_REWARD_V0

  inputs:
    to_wallet_id:
      type: string
      required: true
      description: Destination wallet identifier (validator's wallet)
    amount:
      type: number
      required: true
      description: Reward amount in BACHI
    block_hash:
      type: string
      required: true
      description: Block hash that triggered this reward
    triggered_by:
      type: string
      required: true
      description: System trigger reference

  outcomes:
    ACK:
      description: Reward intent accepted
    NACK:
      description: Reward intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: SYSTEM
```
