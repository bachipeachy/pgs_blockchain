# ENTITY_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** ENTITY_BLOCK_V0
- **Artifact Kind:** entity
- **Governed By:** CONSTITUTION_ENTITY_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare the canonical protocol definition of a **Block** — *what a Block is*, independent of where it
is stored (STRUCTURE), how it is persisted (RUNTIME BINDING), or what is done with it (WORKFLOW/CC).

This is the authoritative source of a Block's identity, attributes, meaning, lifecycle, and invariants.
No CC, WF, Build Sheet, or generator may invent or redefine a Block's fields; they reference this
entity. Once compiled, the normalized entity (via `pi entity blockchain::ENTITY_BLOCK_V0`) is protocol
truth — not this markdown, not runtime data, not any Change Request.

---

## 2. Rationale

A Block's definition was previously undefined at protocol level — it existed only in runtime data and in
transient Change Requests, forcing builders to invent field names. Promoting the entity to a
first-class artifact closes that gap and keeps concerns orthogonal:

- **Entity** — what a Block *is* (this artifact)
- **Structure** — where Blocks are stored (`STRUCTURE_BLOCKCHAIN_STORAGE_V0` references this entity)
- **Runtime Binding** — how the store is accessed
- **Workflow / CC** — what happens to Blocks

A Block is a protocol business object, not a storage schema; generated forms (JSON Schema, SQL DDL)
are projections of this entity, never its source. This is the first real *type declaration* in the
governed type system that happens to execute a blockchain.

---

## 3. Definition

The Machine block declares, as separate addressable layers:

- **authority** — the compiler is the sole *definitional* truth; runtime is observational; a Change
  Request is never the entity's source. (Resolves the "truth by existence" tension explicitly.)
- **projection** — what may feed a projection of this entity (compiler only), the semantic boundary
  `ASSERT_PROJECTION_FIDELITY` enforces.
- **identity** — `block_id`, unique.
- **attributes** — structure only: name, type, cardinality, enum. No meaning here.
- **semantics** — the meaning of each field, kept separate from structure so the two cannot drift.
- **lifecycle** — `status` is a state machine (`PROPOSED → JUSTIFIED → FINALIZED`), not just a field, so
  workflows do not re-invent state logic.
- **relationships** — `proposer → ENTITY_ACTOR_V0` and `transactions → ENTITY_TRANSACTION_V0`, now
  resolved (both entities are declared).
- **invariants** — system-level truths.
- **versioning** — evolution strategy.

Fields are governed reconciliations (§4), not copied from runtime or any CR.

---

## 4. Reconciliation (governed)

Intrinsic-state + semantics-over-layout applied. Consensus concepts are adopted now to position the
protocol for the consensus_pos subdomain; the cryptographic hash is projected, not canonicalized.

| Field(s) | Outcome | Rationale |
|----------|---------|-----------|
| block_id | **Accept** (identity) | canonical identifier (B_<hex>) |
| epoch, round_id, slot, status, is_canonical, timestamp | **Accept** | intrinsic block/consensus state (runtime) |
| height | **Adopt** | block number in the canonical chain — protocol-intrinsic ordering |
| justified_epoch, finalized_epoch | **Adopt** | consensus finality state — belong in the protocol now that consensus_pos is planned (runtime → migration) |
| proposer, transactions | **Adopt as relationships** | `proposer → ACTOR`, `transactions → TRANSACTION` |
| block_hash | **Reject** (projected) | `block_id` is the identity; the hash is not an independently-governed reference today — project, don't canonicalize |

---

## Machine

```yaml
entity_code: ENTITY_BLOCK_V0
artifact_kind: entity
version: v0
governed_by: fb.constitution::CONSTITUTION_ENTITY_V0

core:
  summary: Canonical Block business object
  description: Protocol-level definition of a Block — identity, attributes, semantics, lifecycle, relationships, invariants.
  layer: DOMAINS
  domain: blockchain

  authority:
    primary: compiler                  # the compiled entity is the sole definitional truth
    runtime: observational             # runtime records conform to this entity; they never define it
    change_request: non_definitional   # a CR changes the entity; it is never its source of truth

  projection:
    source_of_truth: compiler
    allowed_sources:
      - blockchain::ENTITY_BLOCK_V0
    forbidden_sources:
      - markdown
      - change_requests
      - runtime_snapshots

  identity:
    field: block_id
    type: string
    unique: true

  attributes:
    - { name: height,          type: integer, cardinality: "1" }
    - { name: epoch,           type: integer, cardinality: "1" }
    - { name: round_id,        type: integer, cardinality: "1" }
    - { name: slot,            type: integer, cardinality: "1" }
    - { name: proposer_id,     type: string,  cardinality: "1" }
    - { name: timestamp,       type: string,  cardinality: "1" }
    - { name: status,          type: string,  cardinality: "1", enum: [PROPOSED, JUSTIFIED, FINALIZED] }
    - { name: is_canonical,    type: boolean, cardinality: "1" }
    - { name: justified_epoch, type: integer, optional: true }
    - { name: finalized_epoch, type: integer, optional: true }
    - { name: tx_ids,          type: array,   item_type: string, cardinality: "0..n" }

  semantics:
    block_id:        "Canonical block identifier (B_<hex>)"
    height:          "Block number in the canonical chain"
    epoch:           "Consensus epoch, derived as slot // 32"
    round_id:        "Consensus round within the epoch"
    slot:            "Total-ordering unit of the consensus timeline"
    proposer_id:     "Actor (A_<hex>) that proposed the block"
    timestamp:       "ISO-8601 block production time"
    status:          "Lifecycle state in the block finalization pipeline (see lifecycle)"
    is_canonical:    "Whether the block is part of the canonical chain"
    justified_epoch: "Consensus epoch in which the block was justified"
    finalized_epoch: "Consensus epoch in which the block was finalized"
    tx_ids:          "Transactions (T_<hex>) included in the block"

  lifecycle:
    field: status
    stages: [PROPOSED, JUSTIFIED, FINALIZED]
    initial: PROPOSED
    terminal: FINALIZED

  relationships:
    - { name: proposer,     field: proposer_id, target: blockchain::ENTITY_ACTOR_V0,       cardinality: one }
    - { name: transactions, field: tx_ids,      target: blockchain::ENTITY_TRANSACTION_V0, cardinality: many }

  invariants:
    - invariant_id: BLOCK_ID_UNIQUE
      constraint: block_id MUST be globally unique

  versioning:
    strategy: semantic
    compatibility: backward_compatible_until_breaking_change
```