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
