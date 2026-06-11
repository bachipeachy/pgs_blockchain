# STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0

## Header (Mandatory)

- **Artifact Code:** STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
- **Artifact Kind:** structure
- **Governed By:** CONSTITUTION_STRUCTURE_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare storage topology for the blockchain orchestration subdomain. Maps the slot clock entity and simulation summary entity to storage implementations and paths. Enforces ownership and simulation isolation invariants.

---

## 2. Rationale

The orchestration subdomain introduces two new entity types not covered by `STRUCTURE_BLOCKCHAIN_STORAGE_V0`:
- **SLOT_CLOCK**: Keyed mutable record tracking the active slot position per simulation run.
- **SIMULATION_SUMMARY**: Append-only journal recording completed simulation outcomes.

Storage paths are a governance concern, not a runtime implementation detail. Declaring them here:
- Provides a single source of truth for orchestration storage topology.
- Decouples CC artifacts from filesystem layout.
- Enforces `simulation_id` as the primary isolation boundary — each simulation run owns exactly one SLOT_CLOCK record; concurrent runs do not collide.
- Enforces ownership invariant — no non-orchestration artifact may directly mutate these stores.

---

## 3. Storage Model

**Principle:** One store per entity type. Subdomain ownership is exclusive.

**Entity Types:**
- SLOT_CLOCK: Keyed mutable record; one active record per `simulation_id`; initialized at simulation launch; advanced per slot execution.
- SIMULATION_SUMMARY: Append-only journal; one record per completed simulation run; immutable after write.

---

## Machine

```yaml
structure_code: STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Blockchain orchestration subdomain storage topology
  description: Maps slot clock and simulation summary entities to storage implementations and paths

  layer: DOMAINS
  domain: blockchain
  subdomain: orchestration

  storage_roots:
    base_path: "{{module_data_root}}"
    description: "Root path for all orchestration subdomain storage (resolved at runtime)"

  entity_stores:
    SLOT_CLOCK:
      description: "Keyed mutable slot clock record (CS_MUTABLE_JSON_V0); one active record per simulation_id; initialized at launch; advanced per slot"
      path: "blockchain/orchestration/state/slot_clock.json"

    SIMULATION_SUMMARY:
      description: "Append-only simulation outcome journal (CS_APPENDONLY_JSONL_V0); one record per completed simulation run; immutable after write"
      path: "blockchain/orchestration/events/simulation_summary.jsonl"

  resolution:
    description: "Runtime path resolution strategy"
    algorithm: "base_path / entity_stores[entity_type].path"
    example: "{{module_data_root}}/blockchain/orchestration/state/slot_clock.json"

  isolation:
    description: "Simulation isolation and ownership constraints"
    rules:
      - "simulation_id is the primary isolation boundary — each simulation run owns exactly one SLOT_CLOCK record"
      - "Concurrent simulation runs identified by distinct simulation_id values do not collide"
      - "No non-orchestration artifact may directly mutate SLOT_CLOCK or SIMULATION_SUMMARY stores"
      - "blockchain::orchestration CCs write only to orchestration stores; cross-subdomain writes are forbidden"
      - "Storage paths resolved via STRUCTURE only — no hardcoded paths in CC or RB artifacts"

  migration:
    description: "Storage migration policy"
    rules:
      - "Path changes are STRUCTURE updates (versioned)"
      - "CC artifacts remain unchanged during migration"
      - "Runtime resolves paths from active STRUCTURE version"
```
