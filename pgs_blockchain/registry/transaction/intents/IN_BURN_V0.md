# IN_BURN_V0

## Header (Mandatory)

- **Artifact Code:** IN_BURN_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_BURN_V0

---

## 1. Intent

Submit a BURN transaction — destroy BACHI by moving it from a wallet to the BURN wallet.

---

## 2. Rationale

BURN is a SYSTEM operation. No actor identity required.
The destination (BURN wallet) is auto-resolved. Only the source wallet and amount are declared.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_BURN_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| from_wallet_id | string | true | Source wallet identifier |
| amount | number | true | Burn amount in BACHI |
| triggered_by | string | true | System trigger reference |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Burn intent accepted |
| NACK | Burn intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** SYSTEM
- **Note:** to_address auto-resolved to BURN wallet; no actor_record; no gas params

---

## Machine

```yaml
in_code: IN_BURN_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit BURN transaction (SYSTEM)
  workflow: WF_BURN_V0

  inputs:
    from_wallet_id:
      type: string
      required: true
      description: Source wallet identifier
    amount:
      type: number
      required: true
      description: Burn amount in BACHI
    triggered_by:
      type: string
      required: true
      description: System trigger reference

  outcomes:
    ACK:
      description: Burn intent accepted
    NACK:
      description: Burn intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: SYSTEM
```
