# CC_HASH_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** CC_HASH_TRANSACTION_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_KECCAK256_HASH_V0

---

## 1. Intent

Compute the keccak-256 hash of the signed transaction bytes.

---

## 2. Rationale

The transaction hash is the canonical identifier for the signed transaction
on the Ethereum network. It is computed after signing and used for indexing,
lookup, and event correlation.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_KECCAK256_HASH_V0 | CT | KECCAK256_HASH |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| signed_tx_bytes | string | true | Hex-encoded signed transaction |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_hash | string | Keccak-256 hash as 0x-prefixed hex (32 bytes) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Hash computed |
| VIOLATION | Invalid input or hash failure |

---

## Machine

```yaml
cc_code: CC_HASH_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Compute keccak-256 hash of signed transaction

  inputs:
    signed_tx_bytes:
      type: string
      required: true

  outputs:
    tx_hash:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: hash_transaction
      transform: capability_transforms::CT_PURE_KECCAK256_HASH_V0
      op: KECCAK256_HASH
      inputs:
        input_bytes: $.inputs.signed_tx_bytes
      outputs:
        tx_hash: $.capability_result.hash_hex
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```
