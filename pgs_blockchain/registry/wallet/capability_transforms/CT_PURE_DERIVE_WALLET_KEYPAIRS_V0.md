# CT_PURE_DERIVE_WALLET_KEYPAIRS_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Intent

Generate entropy, derive an HD wallet master key, and produce dual-address keypairs (EOA + UTXO) from a single seed. Returns only public-derivable fields. All private material (private keys, mnemonic, seed, entropy) is discarded after execution.

---

## 2. Rationale

Wallet creation requires two address types (EOA for account-model, UTXO for transaction-model). Deriving both from a single seed with a shared root path avoids redundant entropy generation and master key computation. This atom composes the full BIP32/BIP39 derivation pipeline internally while exposing only public outputs.

---

## 3. Naming Convention

- **Artifact Code:** CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
- **Operation:** DERIVE_WALLET_KEYPAIRS

---

## 4. Applicability & Non-Applicability

### 4.1 Valid Use Cases

- Generating dual-address keypairs for new wallet creation
- Any HD wallet derivation requiring multiple address types from a single seed

### 4.2 Invalid Use Cases

- Single-address derivation (use appropriate CT_MOLECULE_* instead)
- Key recovery from existing mnemonic (this atom generates new entropy)
- Signing operations (private keys are not returned)

---

## 5. Determinism & Purity Declaration

| Property | Value | Notes |
|----------|-------|-------|
| Deterministic | NO | Generates fresh entropy via OS CSPRNG |
| Purity Class | ct_pure | No persistent state, no side effects |
| Side Effects | NONE | All computation is local |
| Replay Safe | NO | Each invocation produces different keys |

---

## 6. Security Invariant

No output field contains `private_key`, `seed`, `mnemonic`, or `entropy`. These values exist only within the atom's execution scope and are discarded when the function returns. This atom MUST NOT be modified to return private material.

---

## 7. Internal Composition

This atom internally performs the equivalent of:

```
CT_PURE_GENERATE_ENTROPY_V0           → entropy_bytes
CT_PURE_ENTROPY_TO_MNEMONIC_V0        → mnemonic
CT_PURE_MNEMONIC_TO_SEED_V0           → seed_bytes
CT_PURE_DERIVE_MASTER_KEY_V0          → master_key (+ fingerprint)
CT_PURE_DERIVE_CHILD_KEY_V0 foreach   → root_key (m/root_path)
CT_PURE_DERIVE_CHILD_KEY_V0 foreach   → eoa_key (root/eoa_child)
CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0      → eoa_public_key
CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0      → eoa_address
CT_PURE_DERIVE_CHILD_KEY_V0 foreach   → utxo_key (root/utxo_child)
CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0      → utxo_public_key
CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0      → utxo_address
```

Packaged as a single atom because the CC pipeline cannot invoke the same capability code twice with different inputs.

---

## Machine

```yaml
ct_code: CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive dual-address HD wallet keypairs
  description: Generate entropy, derive HD wallet master key, and produce EOA + UTXO keypairs from a single seed
  inputs:
    entropy_bits:
      type: integer
      required: true
      allowed_values: [128, 160, 192, 224, 256]
    entropy_bytes:
      type: hex_string
      required: false
      description: "Optional injected entropy for deterministic testing; overrides OS-generated entropy"
    passphrase:
      type: string
      required: false
      default: ""
    root_path_indices:
      type: array
      required: true
      description: "Hardened root path indices (e.g., [2147483692, 2147483714, 2147483648] for m/44'/66'/0')"
    eoa_child_indices:
      type: array
      required: true
      description: "EOA child path indices, non-hardened (e.g., [0, 0])"
    utxo_child_indices:
      type: array
      required: true
      description: "UTXO child path indices, non-hardened (e.g., [1, 0])"
    curve:
      type: string
      required: false
      default: "secp256k1"
      enum: ["secp256k1", "secp256r1"]
  outputs:
    eoa_public_key_hex:
      type: string
      description: "EOA uncompressed public key, hex-encoded"
    eoa_address:
      type: string
      description: "EOA Ethereum address, 0x-prefixed hex"
    eoa_derivation_path:
      type: string
      description: "Full EOA BIP32 path string (e.g., m/44'/66'/0'/0/0)"
    utxo_public_key_hex:
      type: string
      description: "UTXO uncompressed public key, hex-encoded"
    utxo_address:
      type: string
      description: "UTXO Ethereum address, 0x-prefixed hex"
    utxo_derivation_path:
      type: string
      description: "Full UTXO BIP32 path string (e.g., m/44'/66'/0'/1/0)"
    master_fingerprint:
      type: string
      description: "First 4 bytes of HASH160(master_compressed_pubkey), hex-encoded"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: DERIVE_WALLET_KEYPAIRS
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_derive_wallet_keypairs_v0
    callable: execute
```
