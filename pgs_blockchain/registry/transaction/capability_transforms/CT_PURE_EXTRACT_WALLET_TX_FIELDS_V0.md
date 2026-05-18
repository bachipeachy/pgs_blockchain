# CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Extract transaction-relevant fields from a wallet record, including EOA address
and current nonce.

---

### 2. Rationale

The wallet record stores addresses in arrays and nonce in nested objects.
This atom provides structured extraction for fields needed during transaction
submission, handling array indexing that the expression resolver cannot perform.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
- **Operation:** EXTRACT_WALLET_TX_FIELDS

---

### 4. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same record yields same fields |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure extraction |
| Replay Safe | YES | Deterministic mapping |

---

## Machine

```yaml
ct_code: CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Extract transaction fields from wallet record
  description: Extract transaction-relevant fields from a wallet record, including EOA address and current nonce
  inputs:
    wallet_record:
      type: object
      required: true
  outputs:
    from_address:
      type: string
    current_nonce:
      type: integer
    actor_id:
      type: string

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: EXTRACT_WALLET_TX_FIELDS
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_extract_wallet_tx_fields_v0
    callable: execute
```
