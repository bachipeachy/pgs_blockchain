# ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0

Blockchain Domain CT Surface Closure Assertion

## Machine

```yaml
artifact_code: ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CT_SURFACE_CLOSED_V0

scope:
  applies_to:
    - BLOCKCHAIN

implementation:
  module: pgs_governance.registry.handlers.assert_ct_surface_closed_v0
  callable: execute

allowed_capability_transforms:
  # Domain CTs - Blockchain
  - blockchain::CT_PURE_BUILD_ETH_TRANSACTION_V0
  - blockchain::CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
  - blockchain::CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
  - blockchain::CT_PURE_INCREMENT_WALLET_NONCE_V0
  # Domain CTs - Consensus (PoS)
  - blockchain::CT_PURE_SELECT_PROPOSER_V0
  - blockchain::CT_PURE_DERIVE_SLOT_EPOCH_V0
  # Domain CTs - Chain
  - blockchain::CT_PURE_HASH_BLOCK_V0
  - blockchain::CT_PURE_EXTRACT_PREDECESSOR_HASH_V0
  - blockchain::CT_PURE_DERIVE_BALANCES_V0
```

## Summary

Validates that all blockchain domain capability transforms are explicitly declared.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: Blockchain domain CT artifacts only

## Version History

- **V0**: Initial blockchain CT surface closure (2026-04-23)
- **V0 (surface maintenance, 2026-06-13)**: Declared the consensus (PoS) CTs
  `CT_PURE_SELECT_PROPOSER_V0` and `CT_PURE_DERIVE_SLOT_EPOCH_V0`, bringing the
  declared surface in line with the registry now that closure is enforced from
  this artifact (see `fb.topology::INVARIANT_CT_SURFACE_CLOSED_V0`).
