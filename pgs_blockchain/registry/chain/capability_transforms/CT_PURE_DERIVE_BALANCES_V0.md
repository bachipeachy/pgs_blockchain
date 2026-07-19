# CT_PURE_DERIVE_BALANCES_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_DERIVE_BALANCES_V0
- **Artifact Kind:** capability_transform
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** canonical

---

## 1. Summary

Derive wallet balances from the committed transaction history.

---

## 2. Inputs

| Field | Type |
|---|---|
| committed_history | object |

---

## 3. Outputs

| Field | Type |
|---|---|
| reconciled_balances | object |

---

## Machine

```yaml
ct_code: CT_PURE_DERIVE_BALANCES_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
core:
  summary: Derive wallet balances from the committed transaction history.
  inputs:
    committed_history:
      type: object
      required: true
  outputs:
    reconciled_balances:
      type: object
machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: COMPUTE
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_derive_balances_v0
    callable: execute
```
