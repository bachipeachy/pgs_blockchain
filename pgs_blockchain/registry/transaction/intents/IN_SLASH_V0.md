# IN_SLASH_V0

## Header (Mandatory)

- **Artifact Code:** IN_SLASH_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_SLASH_V0

---

## 1. Intent

Submit a SLASH transaction — penalize a misbehaving validator by moving funds from their wallet to the BURN wallet.

---

## 2. Rationale

SLASH is a SYSTEM operation triggered by consensus penalty detection.
The destination (BURN wallet) is auto-resolved. The source wallet and validator index are declared.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_SLASH_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| from_wallet_id | string | true | Validator's wallet identifier to slash |
| validator_index | integer | true | Validator index being slashed |
| amount | number | true | Slash amount in BACHI |
| triggered_by | string | true | System trigger reference |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Slash intent accepted |
| NACK | Slash intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** SYSTEM
- **Note:** to_address auto-resolved to BURN wallet; no actor_record; no gas params

---

## Machine

```yaml
in_code: IN_SLASH_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit SLASH transaction (SYSTEM)
  workflow: WF_SLASH_V0

  inputs:
    from_wallet_id:
      type: string
      required: true
      description: Validator's wallet identifier to slash
    validator_index:
      type: integer
      required: true
      description: Validator index being slashed
    amount:
      type: number
      required: true
      description: Slash amount in BACHI
    triggered_by:
      type: string
      required: true
      description: System trigger reference

  outcomes:
    ACK:
      description: Slash intent accepted
    NACK:
      description: Slash intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: SYSTEM
```
