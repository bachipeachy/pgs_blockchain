# STRUCTURE_CHAIN_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_CHAIN_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Storage Model

- **chain** — Append-only JSONL store (CS_APPENDONLY_JSONL_V0) → `blockchain/chain/chain.jsonl`
- **chain_head** — Mutable JSON store (CS_MUTABLE_JSON_V0) → `blockchain/chain/chain_head.json`

---

## Machine

```yaml
structure_code: STRUCTURE_CHAIN_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0
core:
  summary: Declare the chain storage (block log and head pointer)
  description: Maps chain entity stores to storage implementations and paths
  layer: DOMAINS
  domain: blockchain
  storage_roots:
    base_path: '{{module_data_root}}'
    description: Root path for all blockchain domain storage (resolved at runtime)
  entity_stores:
    chain:
      description: Append-only JSONL store (CS_APPENDONLY_JSONL_V0)
      path: blockchain/chain/chain.jsonl
    chain_head:
      description: Mutable JSON store (CS_MUTABLE_JSON_V0)
      path: blockchain/chain/chain_head.json
  resolution:
    description: Runtime path resolution strategy
    algorithm: base_path / entity_stores[entity_type].path
    example: '{{module_data_root}}/blockchain/chain/chain.jsonl'
  isolation:
    description: Entity storage isolation constraints
    rules:
    - Each entity type has dedicated storage
    - Cross-entity queries forbidden (no joins)
    - Entity reads must specify entity type explicitly
    - Storage paths resolved via STRUCTURE only
  migration:
    description: Storage migration policy
    rules:
    - Path changes are STRUCTURE updates (versioned)
    - CC artifacts remain unchanged during migration
    - Runtime resolves paths from active STRUCTURE version
```
