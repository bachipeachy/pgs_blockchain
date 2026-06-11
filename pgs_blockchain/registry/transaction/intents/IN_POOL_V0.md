# IN_POOL_V0

## Header (Mandatory)

- **Artifact Code:** IN_POOL_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_POOL_V0

---

## 1. Intent

Submit a POOL transaction — transfer BACHI from the MINT wallet to the POOL wallet to fund staking rewards.

---

## 2. Rationale

POOL is a SYSTEM operation. Both source (MINT) and destination (POOL) wallets are auto-resolved.
Only the amount and trigger reference are required.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_POOL_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| amount | number | true | Pool funding amount in BACHI |
| triggered_by | string | true | System trigger reference |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Pool intent accepted |
| NACK | Pool intent rejected |

---

## 6. Domain

- **Domain:** pgs.blockchain.transaction
- **Authority:** SYSTEM
- **Note:** from_address auto-resolved to MINT wallet; to_address auto-resolved to POOL wallet; no actor_record; no gas params

---

## Machine

```yaml
in_code: IN_POOL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit POOL funding transaction (SYSTEM)
  workflow: WF_POOL_V0

  inputs:
    amount:
      type: number
      required: true
      description: Pool funding amount in BACHI
    triggered_by:
      type: string
      required: true
      description: System trigger reference

  outcomes:
    ACK:
      description: Pool intent accepted
    NACK:
      description: Pool intent rejected

extensions:
  domain: pgs.blockchain.transaction
  authority: SYSTEM
```
