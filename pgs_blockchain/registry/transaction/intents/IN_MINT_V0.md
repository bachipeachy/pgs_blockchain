# IN_MINT_V0

## Header (Mandatory)

- **Artifact Code:** IN_MINT_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_MINT_V0

---

## 1. Intent

Submit a MINT transaction — issue new BACHI from the MINT wallet to a target wallet.

---

## 2. Rationale

MINT is a SYSTEM operation. No actor identity required.
The source (MINT wallet) is auto-resolved. Only the destination wallet and amount are declared.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_MINT_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| to_wallet_id | string | true | Destination wallet identifier |
| amount | number | true | Mint amount in BACHI |
| triggered_by | string | true | System trigger reference (e.g. genesis, reward event) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Mint intent accepted |
| NACK | Mint intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** SYSTEM
- **Note:** from_address auto-resolved to MINT wallet; no actor_record; no gas params

---

## Machine

```yaml
in_code: IN_MINT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit MINT transaction (SYSTEM)
  workflow: WF_MINT_V0

  inputs:
    to_wallet_id:
      type: string
      required: true
      description: Destination wallet identifier
    amount:
      type: number
      required: true
      description: Mint amount in BACHI
    triggered_by:
      type: string
      required: true
      description: System trigger reference

  outcomes:
    ACK:
      description: Mint intent accepted
    NACK:
      description: Mint intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: SYSTEM
```
