# CC_CLAIM_MEMPOOL_TXS_V0

## Header (Mandatory)

- **Artifact Code:** CC_CLAIM_MEMPOOL_TXS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** CC_QUERY_MEMPOOL_TXS_V0 (in WF_PROPOSE_BLOCK_V0 — QUERY remains for read-only inspection)
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Atomically claim all PENDING transactions in the MEMPOOL for a specific proposer, transitioning
them from PENDING to CLAIMED and returning their IDs for block assembly.

---

## 2. Rationale

CC_QUERY_MEMPOOL_TXS_V0 uses a non-atomic LIST + filter pattern: two concurrent slot workers can
both snapshot the same PENDING transactions before either drains, producing double-includes in
separate blocks. This CC replaces it in WF_PROPOSE_BLOCK_V0 with a single atomic UPDATE_WHERE
that claims all PENDING records under a per-file lock, ensuring mutual exclusion at the substrate
level.

Claim ownership (claimed_by: proposer_id) scopes each claim to its proposer. Recovery via
CC_RELEASE_CLAIMED_MEMPOOL_V0 only releases the calling proposer's claims, preventing slot_A's
failure from releasing slot_B's in-flight claims.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | UPDATE_WHERE PENDING→CLAIMED (atomic under per-file lock) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| proposer_id | string | true | Proposer identity; stamped as claimed_by on each claimed record |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_ids | array | IDs of transactions now CLAIMED by this proposer |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | One or more PENDING transactions claimed; tx_ids populated |
| VIOLATION | No PENDING transactions in MEMPOOL (empty or all already CLAIMED) |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION (no PENDING txs) is routed by WF_PROPOSE_BLOCK_V0 → CC_SKIP_ROUND_V0 (valid skip condition)
- BACKEND_ERROR propagates as a hard failure
- On CC_FORM_BLOCK_V0 failure: WF routes to CC_RELEASE_CLAIMED_MEMPOOL_V0 to revert CLAIMED → PENDING

---

## Machine

```yaml
cc_code: CC_CLAIM_MEMPOOL_TXS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Atomically claim PENDING mempool transactions for a proposer; mutual exclusion via per-file lock

  inputs:
    proposer_id:
      type: string
      required: true
      description: Proposer identity stamped on claimed records

  outputs:
    tx_ids:
      type: array
      items:
        type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: claim_pending_txs
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: MEMPOOL
      op: UPDATE_WHERE
      inputs:
        filter:
          status: PENDING
        updates:
          status: CLAIMED
          claimed_by: $.inputs.proposer_id
      outputs:
        tx_ids: $.capability_result.matched_keys
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: mempool
  notes:
    - Replaces CC_QUERY_MEMPOOL_TXS_V0 in WF_PROPOSE_BLOCK_V0; QUERY CC retained for read-only inspection
    - UPDATE_WHERE is atomic under a per-file threading lock — no two concurrent proposers can claim the same PENDING tx
    - claimed_by scopes each claim to its proposer; recovery in CC_RELEASE_CLAIMED_MEMPOOL_V0 is proposer-scoped
    - VIOLATION (no PENDING) routes WF → CC_SKIP_ROUND_V0 (same routing semantics as CC_QUERY_MEMPOOL_TXS_V0 VIOLATION)
    - tx_ids bound from matched_keys (store keys of claimed records)
```
