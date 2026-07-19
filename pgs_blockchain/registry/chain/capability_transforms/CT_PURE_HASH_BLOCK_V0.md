# CT_PURE_HASH_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_HASH_BLOCK_V0
- **Artifact Kind:** capability_transform
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Status:** canonical

---

## 1. Summary

Compute a block's content signature by canonically hashing the block.

---

## 2. Inputs

| Field | Type |
|---|---|
| block | object |

---

## 3. Outputs

| Field | Type |
|---|---|
| content_hash | string |

---

## Machine

```yaml
ct_code: CT_PURE_HASH_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
core:
  summary: Compute a block's content signature by canonically hashing the block.
  inputs:
    block:
      type: object
      required: true
  outputs:
    content_hash:
      type: string
machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: COMPUTE
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_hash_block_v0
    callable: execute
```
