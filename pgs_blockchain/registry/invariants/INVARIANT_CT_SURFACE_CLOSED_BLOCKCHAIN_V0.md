# INVARIANT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0

Blockchain Domain CT Surface Closure Invariant

## Machine

```yaml
invariant_code: INVARIANT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::INVARIANT_CT_SURFACE_CLOSED_V0

core:
  description: >
    All capability transforms used in the blockchain domain must be explicitly
    declared in the closed CT registry for this domain.

    No CT may be referenced in blockchain CC artifacts unless it appears in
    the allowed_capability_transforms list of ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0.

  enforcement_stage:
    - compiler_validation

  scope:
    - BLOCKCHAIN

  violation_response: FAIL_IMMEDIATELY

  enforced_by:
    - blockchain::ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0

  allowed_capability_transforms:
    - blockchain::CT_PURE_BUILD_ETH_TRANSACTION_V0
    - blockchain::CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
    - blockchain::CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
    - blockchain::CT_PURE_INCREMENT_WALLET_NONCE_V0
```

---

## Purpose

Declare the closed set of capability transforms permitted in the blockchain domain.
Any CT reference outside this set is a protocol violation and must stop the build.

---

## Version History

- **V0**: Initial blockchain CT surface closure invariant (2026-04-29)
