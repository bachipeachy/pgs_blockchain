# ENTITY_ACTOR_V0

## Header (Mandatory)

- **Artifact Code:** ENTITY_ACTOR_V0
- **Artifact Kind:** entity
- **Governed By:** CONSTITUTION_ENTITY_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE

---

## 1. Intent

Declare the canonical protocol definition of an **Actor** — the identity root of the blockchain domain
(an Actor owns Wallets, may be a Validator proposer, and is the authority an Intent binds). This is a
**governed reconciliation**, not a copy of runtime or of any Change Request: the compiled entity is the
authoritative Actor definition (`pi entity blockchain::ENTITY_ACTOR_V0`).

---

## 2. Rationale

An Actor's definition lived only in runtime records and a transient data-model Change Request. Promoting
it to a first-class entity gives the identity layer one canonical home. Other entities reference it
(`WALLET.actor_id`, `BLOCK.proposer_id`, `VALIDATOR.actor_id`); none redefine it.

---

## 3. Definition

**Identity:** `actor_id` (`A_<hex>`), unique. **Lifecycle:** `status` is a state machine.
Attributes, semantics, lifecycle and invariants are in the Machine block; the field-by-field governed
decisions are in §4 Reconciliation.

---

## 4. Reconciliation (governed)

Evidence: runtime seed `genesis_actor.json` and the data-model CR (S2 Identity) **agree on every
field** — a clean *Accepted* reconciliation. The CR additionally contributes governed enums and field
meanings (adopted). No contested fields.

| Field | Runtime | CR | Decision | Rationale |
|-------|:---:|:---:|----------|-----------|
| actor_id | ✓ | ✓ | Accepted (identity) | Deterministic unique identifier |
| user_type | ✓ | ✓ | Accepted (enum from CR) | Governed role classification |
| status | ✓ | ✓ | Accepted (lifecycle) | Governed lifecycle states |
| kyc_verified | ✓ | ✓ | Accepted | Verification gate |
| currency_preference | ✓ | ✓ | Accepted | Denomination preference |
| language | ✓ | ✓ | Accepted | Locale preference |
| first_name, last_name | ✓ | ✓ | Accepted | Identity attributes |
| email_registration | ✓ | ✓ | Accepted (unique, immutable) | Registration key |
| created_at, last_modified | ✓ | ✓ | Accepted | Lifecycle timestamps |

No runtime migration required (runtime already conforms).

---

## Machine

```yaml
entity_code: ENTITY_ACTOR_V0
artifact_kind: entity
version: v0
governed_by: fb.constitution::CONSTITUTION_ENTITY_V0

core:
  summary: Canonical Actor business object (identity root)
  description: Protocol-level definition of an Actor — identity, attributes, semantics, lifecycle, invariants.
  layer: DOMAINS
  domain: blockchain

  authority:
    primary: compiler
    runtime: observational
    change_request: non_definitional

  projection:
    source_of_truth: compiler
    allowed_sources:
      - blockchain::ENTITY_ACTOR_V0
    forbidden_sources:
      - markdown
      - change_requests
      - runtime_snapshots

  identity:
    field: actor_id
    type: string
    unique: true

  attributes:
    - { name: user_type,           type: string,  enum: [INDIVIDUAL, BUSINESS, ORGANIZATION, VALIDATOR, DELEGATOR, INSTITUTIONAL, DEVELOPER, TESTNET, GENESIS] }
    - { name: status,              type: string,  enum: [ACTIVE, INACTIVE, SUSPENDED, PENDING, VERIFIED, DELETED] }
    - { name: kyc_verified,        type: boolean }
    - { name: currency_preference, type: string }
    - { name: language,            type: string }
    - { name: first_name,          type: string }
    - { name: last_name,           type: string }
    - { name: email_registration,  type: string }
    - { name: created_at,          type: string }
    - { name: last_modified,       type: string }

  semantics:
    actor_id:            "Deterministic unique actor identifier (A_<hex>)"
    user_type:           "Governed role classification"
    status:              "Identity lifecycle state (see lifecycle)"
    kyc_verified:        "Whether the identity has been verified"
    currency_preference: "Preferred currency denomination (BACHI default)"
    language:            "Preferred language (en default)"
    first_name:          "Given name"
    last_name:           "Family name"
    email_registration:  "Immutable registration email (unique key)"
    created_at:          "Registration timestamp"
    last_modified:       "Last update timestamp"

  lifecycle:
    field: status
    stages: [PENDING, ACTIVE, VERIFIED, SUSPENDED, INACTIVE, DELETED]
    initial: PENDING
    terminal: DELETED

  relationships: []

  invariants:
    - invariant_id: ACTOR_ID_UNIQUE
      constraint: actor_id MUST be globally unique
    - invariant_id: ACTOR_EMAIL_UNIQUE_IMMUTABLE
      constraint: email_registration MUST be unique and immutable after registration

  versioning:
    strategy: semantic
    compatibility: backward_compatible_until_breaking_change
```
