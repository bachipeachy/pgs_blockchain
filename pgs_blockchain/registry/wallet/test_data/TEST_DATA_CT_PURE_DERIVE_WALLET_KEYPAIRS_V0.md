# TEST_DATA_CT_PURE_DERIVE_WALLET_KEYPAIRS_V0

## Machine

```yaml
test_data_code: blockchain::TEST_DATA_CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
  description: |
    Test HD wallet keypair derivation.
  target_artifact: CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_DERIVE_WALLET_KEYPAIRS_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
ct_fqdn: "blockchain::CT_PURE_DERIVE_WALLET_KEYPAIRS_V0"
```

## Purpose

Test HD wallet keypair derivation.

## Test Cases

### Case 1: derive_deterministic_v0

**Description:** Derive keypairs with fixed entropy (injected for testing).

```yaml
case_id: derive_deterministic_v0
expected_outcome: SUCCESS
bindings:
  entropy_bits: 128
  entropy_bytes: "0x000102030405060708090a0b0c0d0e0f"
  passphrase: ""
  root_path_indices: [2147483692, 2147483714, 2147483648]
  eoa_child_indices: [0, 0]
  utxo_child_indices: [1, 0]
  curve: "secp256k1"

expected:
  master_fingerprint: "05d027a5"
  eoa_public_key_hex: "04b554974e8c4211047083db82c0aa87425e924146bf771297368a772ccbe6f9ddce63bc3a8722b88df89f39a2463b42fe47afb4e1437a3b037fe00965beeb424e"
  eoa_address: "0xa147513d04407900191387efaae250f6b5d8b73e"
  eoa_derivation_path: "m/44'/66'/0'/0/0"
  utxo_public_key_hex: "046c494434265132b0ff8b152463b2ebd3fc39510681bf25c439b1ab19929b1ad958ae163406f8ca40a9fe1cb1f6ef086211cebe55007bfc85a27d054c33b9f06c"
  utxo_address: "0xeb1e384387ef200dbab27b1c4b3f3c88683aab52"
  utxo_derivation_path: "m/44'/66'/0'/1/0"
```
