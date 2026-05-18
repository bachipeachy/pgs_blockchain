# CT_PURE_BUILD_ETH_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_BUILD_ETH_TRANSACTION_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE (pure Python RLP encoding)

---

## Human

### 1. Intent

Build an unsigned EIP-1559 (Type 2) Ethereum transaction as RLP-encoded bytes.

This transform accepts all EIP-1559 transaction fields and produces the
canonical unsigned transaction byte representation suitable for signing.

---

### 2. Rationale

EIP-1559 transaction encoding is Ethereum protocol semantics, not a
cryptographic primitive. This atom encodes the transaction structure
per the Ethereum specification. It belongs in the blockchain domain
because RLP encoding is protocol-level logic.

This atom performs **only EIP-1559 RLP encoding**.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_BUILD_ETH_TRANSACTION_V0
- **Operation:** BUILD_ETH_TRANSACTION

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Building unsigned EIP-1559 transactions for signing
- Producing canonical transaction bytes for hash computation

#### 4.2 Invalid Use Cases

- Legacy (pre-EIP-1559) transaction encoding
- Transaction signing (use CT_PURE_ECDSA_SIGN_V0)
- UTXO transaction building

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same fields yield same bytes |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure encoding transform |
| Replay Safe | YES | Deterministic mapping |

---

### 6. Structural Checklist

- [x] Single responsibility
- [x] Deterministic
- [x] No implicit state
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] Fail-loud on invalid input

---

### 7. Composition Rules

As an **atom**, this CT:
- MUST NOT invoke other CTs
- MUST perform exactly one transformation
- MAY be composed by molecules

---

### 8. Validation Expectations

**Runtime validation MUST fail if:**
- Required fields (chain_id, nonce, to, value) are missing
- `to` address is not 20 bytes
- Integer fields cannot be parsed

---

### 9. Observability

This atom does NOT emit domain events.

Unsigned transaction bytes MAY be logged (they contain no secret material).

---

### 10. Security Considerations

- Unsigned transaction bytes contain no secret material
- This atom does not sign or persist — those are separate concerns

---

### 11. Minimal Usage Shape

{chain_id, nonce, to, value, ...} → CT_PURE_BUILD_ETH_TRANSACTION_V0 → unsigned_tx_bytes

---

## Machine

```yaml
ct_code: CT_PURE_BUILD_ETH_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Build unsigned EIP-1559 Ethereum transaction
  description: Build an unsigned EIP-1559 (Type 2) Ethereum transaction as RLP-encoded bytes
  inputs:
    chain_id:
      type: integer
      required: true
    nonce:
      type: integer
      required: true
    max_priority_fee_per_gas:
      type: string
      required: false
      default: "1000000000"
    max_fee_per_gas:
      type: string
      required: false
      default: "20000000000"
    gas_limit:
      type: integer
      required: false
      default: 21000
    to:
      type: string
      required: true
      description: "Destination address as 0x-prefixed hex (20 bytes)"
    value:
      type: string
      required: true
      description: "Transfer value in wei"
    data:
      type: string
      required: false
      default: "0x"
    access_list:
      type: array
      required: false
      default: []
  outputs:
    unsigned_tx_bytes:
      type: string
      description: "EIP-1559 Type 2 unsigned transaction as 0x-prefixed hex"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: BUILD_ETH_TRANSACTION
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_build_eth_transaction_v0
    callable: execute
```
