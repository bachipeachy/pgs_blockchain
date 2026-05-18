# CC_DERIVE_WALLET_KEYS_V0

## Header (Mandatory)

- **Artifact Code:** CC_DERIVE_WALLET_KEYS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_DERIVE_WALLET_KEYPAIRS_V0

---

## 1. Intent

Derive dual-address HD wallet keypairs (EOA + UTXO) for a new wallet. Generates entropy, derives keys through BIP32/BIP39, and returns only public-derivable fields.

---

## 2. Rationale

Wallet key derivation:
- Generates fresh entropy per invocation (no key reuse)
- Derives EOA and UTXO addresses from a single seed with shared root path
- Returns only public keys, addresses, derivation paths, and master fingerprint
- Private material never leaves the CT execution scope

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_DERIVE_WALLET_KEYPAIRS_V0 | CT | DERIVE_WALLET_KEYPAIRS |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| coin_type | integer | false | BIP44 coin type (default 66 for BACHI) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| eoa_public_key_hex | string | EOA uncompressed public key, hex |
| eoa_address | string | EOA Ethereum address, 0x-prefixed |
| eoa_derivation_path | string | Full EOA BIP32 path |
| utxo_public_key_hex | string | UTXO uncompressed public key, hex |
| utxo_address | string | UTXO Ethereum address, 0x-prefixed |
| utxo_derivation_path | string | Full UTXO BIP32 path |
| master_fingerprint | string | HASH160(master_pubkey)[:4], hex |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Key derivation completed |
| VIOLATION | Invalid input or CT execution failure |

---

## 7. Failure Semantics

- CT failure results in VIOLATION and exit
- No side effects on failure — entropy is discarded

---

## 8. Security Invariant

No CT output field containing `private_key`, `seed`, `mnemonic`, or `entropy` may be bound to any CS or persistent capability. Only the output fields listed in §5 appear in the CC output bindings. Private material exists only within the CT execution scope and is discarded when the pipeline completes.

---

## 9. Derivation Path Semantics

```
derivation_root = m/44'/66'/0'     (purpose / coin_type / account — all hardened)
child paths (relative to root):
  EOA  = 0/0                        (change=0 / address_index=0 — NOT hardened)
  UTXO = 1/0                        (change=1 / address_index=0 — NOT hardened)

Full resolved paths:
  EOA  = m/44'/66'/0'/0/0
  UTXO = m/44'/66'/0'/1/0
```

The derivation_root includes account-level hardening. Child path indices are non-hardened. Do not double-harden.

---

## Machine

```yaml
cc_code: CC_DERIVE_WALLET_KEYS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Derive dual-address HD wallet keypairs

  inputs:
    coin_type:
      type: integer
      required: false

  outputs:
    eoa_public_key_hex:
      type: string
    eoa_address:
      type: string
    eoa_derivation_path:
      type: string
    utxo_public_key_hex:
      type: string
    utxo_address:
      type: string
    utxo_derivation_path:
      type: string
    master_fingerprint:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: derive_wallet_keypairs
      transform: blockchain::CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
      op: DERIVE_WALLET_KEYPAIRS
      inputs:
        entropy_bits: 128
        passphrase: ""
        root_path_indices: [2147483692, 2147483714, 2147483648]
        eoa_child_indices: [0, 0]
        utxo_child_indices: [1, 0]
        curve: secp256k1
      outputs:
        eoa_public_key_hex: $.capability_result.eoa_public_key_hex
        eoa_address: $.capability_result.eoa_address
        eoa_derivation_path: $.capability_result.eoa_derivation_path
        utxo_public_key_hex: $.capability_result.utxo_public_key_hex
        utxo_address: $.capability_result.utxo_address
        utxo_derivation_path: $.capability_result.utxo_derivation_path
        master_fingerprint: $.capability_result.master_fingerprint
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```
