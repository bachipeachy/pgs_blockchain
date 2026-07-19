# CT_PURE_EXTRACT_PREDECESSOR_HASH_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_EXTRACT_PREDECESSOR_HASH_V0
- **Artifact Kind:** capability_transform
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** canonical

---

## 1. Summary

Extract the predecessor hash carried by a proposed block.

---

## 2. Inputs

| Field | Type |
|---|---|
| block | object |

---

## 3. Outputs

| Field | Type |
|---|---|
| predecessor_hash | string |

---

## Machine

```yaml
ct_code: CT_PURE_EXTRACT_PREDECESSOR_HASH_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
core:
  summary: Extract the predecessor hash carried by a proposed block.
  inputs:
    block:
      type: object
      required: true
  outputs:
    predecessor_hash:
      type: string
machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: COMPUTE
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_extract_predecessor_hash_v0
    callable: execute
```
