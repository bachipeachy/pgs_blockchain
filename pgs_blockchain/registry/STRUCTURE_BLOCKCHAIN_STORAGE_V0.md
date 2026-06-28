# STRUCTURE_BLOCKCHAIN_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_BLOCKCHAIN_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare storage topology for blockchain domain entities. Maps entity types to storage implementations and paths.

---

## 2. Rationale

Storage paths are governance concern, not runtime implementation detail. This STRUCTURE artifact:
- Centralizes storage topology (single source of truth)
- Decouples CC artifacts from filesystem layout
- Enables storage migration without CC changes
- Enforces entity-level isolation (WALLET ≠ TRANSACTION)

---

## 3. Storage Model

**Principle:** One store per domain entity type.

**Entity Types:**
- ACTOR: Identity registry
- WALLET: Wallet state
- TRANSACTION: Transaction state
- WALLET_EVENTS: Wallet lifecycle events
- TRANSACTION_EVENTS: Transaction lifecycle events
- ACTOR_EVENTS: Actor lifecycle events
- VALIDATOR: Validator registry (actor_id → validator record pointer)
- VALIDATOR_EVENTS: Validator lifecycle events
- CONSENSUS_ROUNDS: Consensus round journal (append-only)
- CONSENSUS_EVENTS: Consensus lifecycle event journal (append-only)
- BLOCKS: Block state storage (mutable)
- BLOCK_EVENTS: Block lifecycle event journal (append-only)
- MEMPOOL: Ephemeral pending transaction staging buffer (CS_MUTABLE_JSON_V0)
- MEMPOOL_INDEX: Mempool deduplication registry for tx_id and tx_hash uniqueness (CS_REGISTRY_V0)

---

## Machine

```yaml
structure_code: STRUCTURE_BLOCKCHAIN_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Blockchain domain storage topology
  description: Maps entity types to storage implementations and paths

  layer: DOMAINS
  domain: blockchain

  storage_roots:
    base_path: "{{module_data_root}}"
    description: "Root path for all blockchain domain storage (resolved at runtime)"

  entity_stores:
    ACTOR:
      description: "Actor identity registry (KYC → actor_id resolution)"
      path: "blockchain/identity/registry/actors.json"

    WALLET:
      description: "Wallet state storage (wallet_id → wallet record)"
      path: "blockchain/wallet/state/wallets.json"

    TRANSACTION:
      description: "Transaction state storage (tx_id → transaction record)"
      path: "blockchain/transaction/state/transactions.json"

    WALLET_EVENTS:
      description: "Wallet lifecycle event journal"
      path: "blockchain/wallet/events/wallet_events.jsonl"

    TRANSACTION_EVENTS:
      description: "Transaction lifecycle event journal"
      path: "blockchain/transaction/events/transaction_events.jsonl"

    ACTOR_EVENTS:
      description: "Actor lifecycle event journal"
      path: "blockchain/identity/events/identity_events.jsonl"

    VALIDATOR:
      description: "Validator registry (actor_id → validator record; CS_MUTABLE_JSON_V0)"
      path: "blockchain/consensus_pos/registry/validators.json"

    VALIDATOR_EVENTS:
      description: "Validator lifecycle event journal"
      path: "blockchain/consensus_pos/events/validator_events.jsonl"

    CONSENSUS_ROUNDS:
      description: "Consensus round journal (CS_APPENDONLY_JSONL_V0)"
      path: "blockchain/consensus_pos/rounds/rounds.jsonl"

    CONSENSUS_EVENTS:
      description: "Consensus lifecycle event journal (CS_APPENDONLY_JSONL_V0)"
      path: "blockchain/consensus_pos/events/consensus_events.jsonl"

    BLOCKS:
      description: "Block state storage (block_id → block record; CS_MUTABLE_JSON_V0)"
      path: "blockchain/block/blocks/blocks.json"
      record_type: blockchain::ENTITY_BLOCK_V0   # the canonical Block entity (what a block IS)

    BLOCK_EVENTS:
      description: "Block lifecycle event journal (CS_APPENDONLY_JSONL_V0)"
      path: "blockchain/block/events/block_events.jsonl"

    MEMPOOL:
      description: "Ephemeral staging buffer for pending transactions (CS_MUTABLE_JSON_V0); keyed by tx_id; deleted on drain"
      path: "blockchain/mempool/state/mempool.json"

    MEMPOOL_INDEX:
      description: "Deduplication registry for tx_id and tx_hash uniqueness (CS_REGISTRY_V0)"
      path: "blockchain/mempool/registry/mempool_index.json"

  resolution:
    description: "Runtime path resolution strategy"
    algorithm: "base_path / entity_stores[entity_type].path"
    example: "{{module_data_root}}/blockchain/wallet/state/wallets.json"

  isolation:
    description: "Entity storage isolation constraints"
    rules:
      - "Each entity type has dedicated storage"
      - "Cross-entity queries forbidden (no joins)"
      - "Entity reads must specify entity type explicitly"
      - "Storage paths resolved via STRUCTURE only"

  migration:
    description: "Storage migration policy"
    rules:
      - "Path changes are STRUCTURE updates (versioned)"
      - "CC artifacts remain unchanged during migration"
      - "Runtime resolves paths from active STRUCTURE version"
```
