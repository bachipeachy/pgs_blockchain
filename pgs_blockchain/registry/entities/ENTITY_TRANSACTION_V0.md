# ENTITY_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** ENTITY_TRANSACTION_V0
- **Artifact Kind:** entity
- **Governed By:** CONSTITUTION_ENTITY_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare the canonical protocol definition of a **Transaction** — a governed value movement authorized by
an Actor, optionally between Wallets, optionally included in a Block. A governed reconciliation modeling
protocol *semantics*, not the EVM-shaped implementation layout an earlier CR carried.

---

## 2. Rationale

The transaction definition had diverged badly: runtime stored a thin event with a nested `payload`; the
data-model CR carried a 20-field EVM-gas schema, most of it JIT-computed. This entity keeps only intrinsic
protocol state and expresses block inclusion and the parties as *relationships*, not duplicated ids.

---

## 3. Definition

**Identity:** `tx_id` (`T_<hex>`). **Lifecycle:** `status`. **Relationships:** `authorized_by → ACTOR`,
`from`/`to → WALLET` (asymmetric by tx_type), `included_in → BLOCK`. Governed decisions in §4.

---

## 4. Reconciliation (governed)

Intrinsic-state + semantics-over-layout applied (relationships preferred over duplicated identifiers;
derived/abandoned-design values rejected).

| Field(s) | Outcome | Rationale |
|----------|---------|-----------|
| tx_id | **Accept** (identity) | canonical identifier |
| tx_type, amount, currency, status, timestamp | **Accept** | intrinsic transaction state |
| parties / inclusion | **Adopt as relationships** | `authorized_by → ACTOR`, `from`/`to → WALLET`, `included_in → BLOCK` |
| nonce | **Defer** | intrinsic concept, no governed consumer; null for system txs |
| tx_hash | **Reject** (projected) | not the identity; not independently-governed reference today |
| block_number, block_hash | **Reject** | block inclusion is the `included_in` relationship, not duplicated ids |
| gas_limit, max_fee_per_gas, max_priority_fee_per_gas, base_fee_per_gas, effective_gas_price, gas_used, total_fee | **Reject** | the protocol has NOT adopted a resource-accounting model; EVM gas is an abandoned design direction, not a protocol concept — returns only via a fresh CR |
| network | **Reject** | deployment context, not transaction state |
| memo | **Reject** | presentation |
| payload, event_code | **Reject** | runtime event-wrapper implementation nesting |

Migration: the EVM gas vocabulary is dropped; a future resource-accounting CR introduces its own.

---

## Machine

```yaml
entity_code: ENTITY_TRANSACTION_V0
artifact_kind: entity
version: v0
governed_by: fb.constitution::CONSTITUTION_ENTITY_V0

core:
  summary: Canonical Transaction business object (governed value movement)
  description: Protocol-level definition of a Transaction — identity, intrinsic attributes, semantics, lifecycle, relationships, invariants.
  layer: DOMAINS
  domain: blockchain

  authority:
    primary: compiler
    runtime: observational
    change_request: non_definitional

  projection:
    source_of_truth: compiler
    allowed_sources:
      - blockchain::ENTITY_TRANSACTION_V0
    forbidden_sources:
      - markdown
      - change_requests
      - runtime_snapshots

  identity:
    field: tx_id
    type: string
    unique: true

  attributes:
    - { name: tx_type,      type: string, enum: [TRANSFER, MINT, BURN, POOL, STAKE, UNSTAKE, REWARD, SLASH] }
    - { name: amount,       type: number }
    - { name: currency,     type: string }
    - { name: status,       type: string, enum: [PENDING, SUBMITTED, INCLUDED, FINALIZED, FAILED] }
    - { name: timestamp,    type: string }
    - { name: initiated_by, type: string }                     # actor_id of the authorizing actor
    - { name: from_wallet,  type: string, optional: true }     # null for MINT / REWARD (system-sourced)
    - { name: to_wallet,    type: string, optional: true }     # null for SLASH / BURN (protocol-routed)
    - { name: in_block,     type: string, optional: true }     # block_id once included (else null)

  semantics:
    tx_id:        "Canonical transaction identifier (T_<hex>)"
    tx_type:      "Governed transaction classification"
    amount:       "Value moved, in the stated currency"
    currency:     "Denomination (BACHI)"
    status:       "Transaction lifecycle state (see lifecycle)"
    timestamp:    "Submission time"
    initiated_by: "Actor that authorized the transaction (A_<hex>)"
    from_wallet:  "Source wallet (W_<hex>); absent for system-sourced types"
    to_wallet:    "Destination wallet (W_<hex>); absent for protocol-routed types"
    in_block:     "Including block once finalized; absent while pending"

  lifecycle:
    field: status
    stages: [PENDING, SUBMITTED, INCLUDED, FINALIZED, FAILED]
    initial: PENDING
    terminal: FINALIZED

  relationships:
    - { name: authorized_by, field: initiated_by, target: blockchain::ENTITY_ACTOR_V0,  cardinality: one }
    - { name: from,          field: from_wallet,  target: blockchain::ENTITY_WALLET_V0, cardinality: zero_or_one }
    - { name: to,            field: to_wallet,    target: blockchain::ENTITY_WALLET_V0, cardinality: zero_or_one }
    - { name: included_in,   field: in_block,     target: blockchain::ENTITY_BLOCK_V0,  cardinality: zero_or_one }

  invariants:
    - invariant_id: TX_ID_UNIQUE
      constraint: tx_id MUST be globally unique
    - invariant_id: TX_AMOUNT_NONNEGATIVE
      constraint: amount MUST NOT be negative
    - invariant_id: TX_AUTHORIZED
      constraint: initiated_by MUST reference a valid blockchain::ENTITY_ACTOR_V0

  versioning:
    strategy: semantic
    compatibility: backward_compatible_until_breaking_change
```
