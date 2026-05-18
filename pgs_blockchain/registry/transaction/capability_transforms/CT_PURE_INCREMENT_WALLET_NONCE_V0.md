# CT_PURE_INCREMENT_WALLET_NONCE_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_INCREMENT_WALLET_NONCE_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Create a copy of a wallet record with the EOA nonce incremented by 1,
returning both the updated record and the reserved nonce value.

---

### 2. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same record yields same result |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure transform |
| Replay Safe | YES | Deterministic mapping |

---

## Machine

```yaml
ct_code: CT_PURE_INCREMENT_WALLET_NONCE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Increment wallet EOA nonce and return reserved value
  description: Create a copy of a wallet record with the EOA nonce incremented by 1, returning both the updated record and the reserved nonce value
  inputs:
    wallet_record:
      type: object
      required: true
  outputs:
    updated_wallet_record:
      type: object
    nonce:
      type: integer

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: INCREMENT_WALLET_NONCE
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_increment_wallet_nonce_v0
    callable: execute
```
