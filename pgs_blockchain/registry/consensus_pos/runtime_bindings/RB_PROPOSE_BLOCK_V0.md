# RB_PROPOSE_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** RB_PROPOSE_BLOCK_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the block proposal workflow, covering multi-store mutable JSON access (VALIDATOR, MEMPOOL, and BLOCKS stores) and append-only journal writes (CONSENSUS_ROUNDS, CONSENSUS_EVENTS, and BLOCK_EVENTS stores).

---

## 2. Scope

Supports:

- Mutable JSON binding for VALIDATOR, MEMPOOL, and BLOCKS stores (store-resolved via STRUCTURE_BLOCKCHAIN_STORAGE_V0)
- Append-only journal binding for CONSENSUS_ROUNDS, CONSENSUS_EVENTS, and BLOCK_EVENTS stores (store-resolved via STRUCTURE_BLOCKCHAIN_STORAGE_V0)

All store paths are declared in STRUCTURE_BLOCKCHAIN_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_PROPOSE_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for block proposal workflow
  description: Binds capability side effects to concrete runtime implementations for block proposal. Covers MEMPOOL store access (CC_QUERY_MEMPOOL_TXS_V0, CC_DRAIN_MEMPOOL_V0) and settled storage (VALIDATOR, BLOCKS, CONSENSUS_ROUNDS, CONSENSUS_EVENTS, BLOCK_EVENTS). All store paths resolved from STRUCTURE_BLOCKCHAIN_STORAGE_V0.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}
```
