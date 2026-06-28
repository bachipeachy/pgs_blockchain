# ENTITY_WALLET_V0

## Header (Mandatory)

- **Artifact Code:** ENTITY_WALLET_V0
- **Artifact Kind:** entity
- **Governed By:** CONSTITUTION_ENTITY_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare the canonical protocol definition of a **Wallet** — the balance/aggregation state owned by an
Actor. A governed reconciliation, not a copy of runtime or any Change Request.

---

## 2. Rationale

A Wallet's definition diverged across runtime and the data-model CR. This entity is the single canonical
home; `actor_id` references the Actor identity (`ENTITY_ACTOR_V0`).

---

## 3. Definition

**Identity:** `wallet_id`. **Lifecycle:** `status`. **Owner:** `actor_id → ENTITY_ACTOR_V0`.
Field-by-field governed decisions are in §4 Reconciliation.

---

## 4. Reconciliation (governed)

Intrinsic-state rule applied: canonicalize a field only if it is intrinsic protocol state; project
derived/observational/implementation-specific data.

| Field | Runtime | CR | Outcome | Rationale |
|-------|:--:|:--:|---------|-----------|
| wallet_id | ✓ | ✓ | **Accept** (identity) | governed identifier |
| actor_id | ✓ | ✓ | **Accept** (→ ENTITY_ACTOR_V0) | owning identity |
| balance | ✓ | ✓ | **Accept** | intrinsic ledger state |
| status | ✓ | ✓ | **Accept** (lifecycle) | governed lifecycle |
| wallet_type | ✓ | ✓ | **Accept** (enum, uppercase) | CR governs the enum; runtime casing drift (`business`) → migration |
| address | ✓ | ✗ | **Adopt** | wallet's on-chain identity — intrinsic |
| currency | ✓ | ✗ | **Adopt** | governed denomination |
| created_at, last_modified | ✓ | ✗ | **Adopt** | lifecycle timestamps |
| state (`{eoa:{nonce}}`) | ✓ | ✗ | **Reject** | EOA-style implementation wrapper, not intrinsic protocol state |
| nonce | ✓(nested) | ✓ | **Defer** | intrinsic concept (replay/ordering) but no governed consumer yet; exists dormant at `state.eoa.nonce` — Adopt (flat) when tx ordering becomes a protocol requirement |
| name | ✗ | ✓ | **Reject** | presentation label, not protocol identity |
| last_tx_at | ✗ | ✓ | **Reject** | derivable from transaction history — project, never canonicalize |

Migrations: `wallet_type` casing → uppercase; `state.eoa` wrapper retired if/when `nonce` is adopted flat.

---

## Machine

```yaml
entity_code: ENTITY_WALLET_V0
artifact_kind: entity
version: v0
governed_by: fb.constitution::CONSTITUTION_ENTITY_V0

core:
  summary: Canonical Wallet business object (balance state owned by an Actor)
  description: Protocol-level definition of a Wallet — identity, attributes, semantics, lifecycle, relationships, invariants.
  layer: DOMAINS
  domain: blockchain

  authority:
    primary: compiler
    runtime: observational
    change_request: non_definitional

  projection:
    source_of_truth: compiler
    allowed_sources:
      - blockchain::ENTITY_WALLET_V0
    forbidden_sources:
      - markdown
      - change_requests
      - runtime_snapshots

  identity:
    field: wallet_id
    type: string
    unique: true

  attributes:
    - { name: actor_id,      type: string }
    - { name: address,       type: string }
    - { name: balance,       type: number }
    - { name: currency,      type: string }
    - { name: status,        type: string, enum: [ACTIVE, INACTIVE, CLOSED] }
    - { name: wallet_type,   type: string, enum: [DEFAULT, PRIVATE, BUSINESS, SAVINGS, INVESTMENT, MINT, BURN, POOL] }
    - { name: created_at,    type: string }
    - { name: last_modified, type: string }

  semantics:
    wallet_id:     "Governed wallet identifier"
    actor_id:      "Owning actor (A_<hex>)"
    address:       "Wallet on-chain address"
    balance:       "Current ledger balance"
    currency:      "Denomination (BACHI default)"
    status:        "Wallet lifecycle state (see lifecycle)"
    wallet_type:   "Governed wallet classification"
    created_at:    "Creation timestamp"
    last_modified: "Last update timestamp"

  lifecycle:
    field: status
    stages: [ACTIVE, INACTIVE, CLOSED]
    initial: ACTIVE
    terminal: CLOSED

  relationships:
    - name: owner
      field: actor_id
      target: blockchain::ENTITY_ACTOR_V0
      cardinality: one

  invariants:
    - invariant_id: WALLET_ID_UNIQUE
      constraint: wallet_id MUST be globally unique
    - invariant_id: WALLET_BALANCE_NONNEGATIVE
      constraint: balance MUST NOT be negative
    - invariant_id: WALLET_OWNER_EXISTS
      constraint: actor_id MUST reference a valid blockchain::ENTITY_ACTOR_V0

  versioning:
    strategy: semantic
    compatibility: backward_compatible_until_breaking_change
```
