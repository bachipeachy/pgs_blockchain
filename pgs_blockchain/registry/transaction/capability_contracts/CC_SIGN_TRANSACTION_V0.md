# CC_SIGN_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** CC_SIGN_TRANSACTION_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_MNEMONIC_TO_SEED_V0, CT_PURE_DERIVE_MASTER_KEY_V0, CT_PURE_DERIVE_CHILD_KEY_V0, CT_PURE_KECCAK256_HASH_V0, CT_PURE_ECDSA_SIGN_V0

---

## 1. Intent

Re-derive the private key from a user-supplied mnemonic and sign the unsigned transaction.

---

## 2. Rationale

Bring-your-own-mnemonic signing model: the user supplies the mnemonic in the payload.
The system re-derives the private key at the exact BIP32 path stored in the wallet
record, signs, and discards all secret material. The mnemonic is never persisted.

**Security invariant:** No field containing private_key, seed, mnemonic, or entropy
may be bound to any CS output.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_MNEMONIC_TO_SEED_V0 | CT | MNEMONIC_TO_SEED |
| 2 | CT_PURE_DERIVE_MASTER_KEY_V0 | CT | DERIVE_MASTER_KEY |
| 3 | CT_PURE_DERIVE_CHILD_KEY_V0 | CT | DERIVE_CHILD_KEY (44') |
| 4 | CT_PURE_DERIVE_CHILD_KEY_V0 | CT | DERIVE_CHILD_KEY (66') |
| 5 | CT_PURE_DERIVE_CHILD_KEY_V0 | CT | DERIVE_CHILD_KEY (0') |
| 6 | CT_PURE_DERIVE_CHILD_KEY_V0 | CT | DERIVE_CHILD_KEY (0) |
| 7 | CT_PURE_DERIVE_CHILD_KEY_V0 | CT | DERIVE_CHILD_KEY (0) |
| 8 | CT_PURE_KECCAK256_HASH_V0 | CT | KECCAK256_HASH |
| 9 | CT_PURE_ECDSA_SIGN_V0 | CT | ECDSA_SIGN |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| mnemonic | string | true | BIP-39 mnemonic (transient secret) |
| unsigned_tx_bytes | string | true | Hex-encoded unsigned transaction |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| signature | object | {v, r, s} signature components |
| signed_tx_bytes | string | Full signed transaction bytes (hex) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Transaction signed successfully |
| VIOLATION | Key derivation or signing failure (TX_SIGNING_FAILED) |

---

## 7. Trace Suppression

```yaml
suppress_trace_fields:
  - mnemonic
  - seed
  - private_key
  - entropy
```

---

## Machine

```yaml
cc_code: CC_SIGN_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Re-derive key from mnemonic and sign transaction

  suppress_trace_fields:
    - mnemonic
    - seed
    - private_key
    - entropy
    - seed_bytes
    - private_key_bytes
    - key_and_address
    - master_private_key_bytes
    - master_chain_code_bytes
    - child_private_key_bytes
    - child_chain_code_bytes
    - eoa_private_key_bytes

  inputs:
    mnemonic:
      type: string
      required: true
      description: "BIP-39 mnemonic for key derivation"
    unsigned_tx_bytes:
      type: string
      required: true
      description: "Unsigned transaction bytes (hex-encoded)"

  outputs:
    signature:
      type: object
    signed_tx_bytes:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: mnemonic_to_seed
      transform: capability_transforms::CT_PURE_MNEMONIC_TO_SEED_V0
      op: MNEMONIC_TO_SEED
      inputs:
        mnemonic: $.inputs.mnemonic
      outputs:
        seed_bytes: $.capability_result.seed_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_master_key
      transform: capability_transforms::CT_PURE_DERIVE_MASTER_KEY_V0
      op: DERIVE_MASTER_KEY
      inputs:
        seed_bytes: $.results.mnemonic_to_seed.seed_bytes
      outputs:
        master_private_key_bytes: $.capability_result.master_private_key_bytes
        master_chain_code_bytes: $.capability_result.master_chain_code_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_44h
      transform: capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
      op: DERIVE_CHILD_KEY
      inputs:
        parent_private_key_bytes: $.results.derive_master_key.master_private_key_bytes
        parent_chain_code_bytes: $.results.derive_master_key.master_chain_code_bytes
        index: 2147483692
      outputs:
        child_private_key_bytes: $.capability_result.child_private_key_bytes
        child_chain_code_bytes: $.capability_result.child_chain_code_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_66h
      transform: capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
      op: DERIVE_CHILD_KEY
      inputs:
        parent_private_key_bytes: $.results.derive_44h.child_private_key_bytes
        parent_chain_code_bytes: $.results.derive_44h.child_chain_code_bytes
        index: 2147483714
      outputs:
        child_private_key_bytes: $.capability_result.child_private_key_bytes
        child_chain_code_bytes: $.capability_result.child_chain_code_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_0h
      transform: capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
      op: DERIVE_CHILD_KEY
      inputs:
        parent_private_key_bytes: $.results.derive_66h.child_private_key_bytes
        parent_chain_code_bytes: $.results.derive_66h.child_chain_code_bytes
        index: 2147483648
      outputs:
        child_private_key_bytes: $.capability_result.child_private_key_bytes
        child_chain_code_bytes: $.capability_result.child_chain_code_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_0_change
      transform: capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
      op: DERIVE_CHILD_KEY
      inputs:
        parent_private_key_bytes: $.results.derive_0h.child_private_key_bytes
        parent_chain_code_bytes: $.results.derive_0h.child_chain_code_bytes
        index: 0
      outputs:
        child_private_key_bytes: $.capability_result.child_private_key_bytes
        child_chain_code_bytes: $.capability_result.child_chain_code_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: derive_0_address
      transform: capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
      op: DERIVE_CHILD_KEY
      inputs:
        parent_private_key_bytes: $.results.derive_0_change.child_private_key_bytes
        parent_chain_code_bytes: $.results.derive_0_change.child_chain_code_bytes
        index: 0
      outputs:
        eoa_private_key_bytes: $.capability_result.child_private_key_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: hash_unsigned_tx
      transform: capability_transforms::CT_PURE_KECCAK256_HASH_V0
      op: KECCAK256_HASH
      inputs:
        input_bytes: $.inputs.unsigned_tx_bytes
      outputs:
        message_hash: $.capability_result.hash_hex
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: sign_tx_hash
      transform: capability_transforms::CT_PURE_ECDSA_SIGN_V0
      op: ECDSA_SIGN
      inputs:
        private_key_bytes: $.results.derive_0_address.eoa_private_key_bytes
        message_hash: $.results.hash_unsigned_tx.message_hash
        curve: secp256k1
      outputs:
        signature:
          v: $.capability_result.v
          r: $.capability_result.r
          s: $.capability_result.s
        signed_tx_bytes: $.capability_result.signed_bytes
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

  error_codes:
    VIOLATION: TX_SIGNING_FAILED
```
