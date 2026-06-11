# RB_SUBMIT_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** RB_SUBMIT_TRANSACTION_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the transaction submission workflow, covering mutable JSON access for MEMPOOL and ACTOR stores, registry access for MEMPOOL_INDEX and ACTOR identity registry, and append-only journal writes for TRANSACTION_EVENTS.

---

## 2. Scope

Supports:

- Registry binding for MEMPOOL_INDEX (deduplication) and ACTOR identity (actor resolution) — store-resolved via STRUCTURE_BLOCKCHAIN_STORAGE_V0
- Mutable JSON binding for MEMPOOL store (pending transaction staging) — store-resolved via STRUCTURE_BLOCKCHAIN_STORAGE_V0
- Append-only journal binding for TRANSACTION_EVENTS store — store-resolved via STRUCTURE_BLOCKCHAIN_STORAGE_V0

All store paths are declared in STRUCTURE_BLOCKCHAIN_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_SUBMIT_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for transaction submission workflow
  description: Binds capability side effects to concrete runtime implementations for transaction submission. All store paths resolved from STRUCTURE_BLOCKCHAIN_STORAGE_V0.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy: {}

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}

    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
```