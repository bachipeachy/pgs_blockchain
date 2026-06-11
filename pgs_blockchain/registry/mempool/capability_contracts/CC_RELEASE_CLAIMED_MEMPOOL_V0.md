# CC_RELEASE_CLAIMED_MEMPOOL_V0

## Header (Mandatory)

- **Artifact Code:** CC_RELEASE_CLAIMED_MEMPOOL_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Release a proposer's CLAIMED transactions back to PENDING when block formation fails, preventing
claimed transactions from being permanently stranded in the CLAIMED state.

---

## 2. Rationale

CC_CLAIM_MEMPOOL_TXS_V0 transitions PENDING → CLAIMED with claimed_by stamped to the proposer.
If CC_FORM_BLOCK_V0 fails (VIOLATION or BACKEND_ERROR), the claimed transactions would be stuck
as CLAIMED and invisible to future proposers' PENDING queries — a liveness bug.

This CC is the recovery path: it reverses CLAIMED → PENDING for the specific proposer only.
Scoping the filter to {status: CLAIMED, claimed_by: proposer_id} ensures that a failing slot_A
does not accidentally release slot_B's in-flight claims.

VIOLATION (nothing to release) is treated as idempotent success at the WF level — the proposer
may have already been cleaned up or never successfully claimed.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | UPDATE_WHERE CLAIMED→PENDING (scoped to this proposer) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| proposer_id | string | true | Proposer whose claims are to be released |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| released_count | integer | Number of transactions reverted to PENDING |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | One or more CLAIMED transactions released back to PENDING |
| VIOLATION | No CLAIMED transactions found for this proposer (idempotent — treated as clean) |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION (nothing to release) is acceptable — routed to EXIT by WF (idempotent recovery)
- BACKEND_ERROR propagates as a hard failure
- claimed_by: null removes the ownership field, returning the record to clean PENDING state

---

## Machine

```yaml
cc_code: CC_RELEASE_CLAIMED_MEMPOOL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Release a proposer's CLAIMED mempool transactions back to PENDING on block formation failure

  inputs:
    proposer_id:
      type: string
      required: true
      description: Proposer whose CLAIMED transactions are to be reverted to PENDING

  outputs:
    released_count:
      type: integer
      description: Number of transactions reverted to PENDING

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: release_claimed_txs
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: MEMPOOL
      op: UPDATE_WHERE
      inputs:
        filter:
          status: CLAIMED
          claimed_by: $.inputs.proposer_id
        updates:
          status: PENDING
          claimed_by: null
      outputs:
        released_count: $.capability_result.updated_count
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: mempool
  notes:
    - Recovery path invoked by WF_PROPOSE_BLOCK_V0 on CC_FORM_BLOCK_V0 VIOLATION or BACKEND_ERROR
    - "Filter is proposer-scoped — {status: CLAIMED, claimed_by: proposer_id} — never releases peer proposers' claims"
    - claimed_by: null removes the field from the record (UPDATE_WHERE null-value semantics = field deletion)
    - VIOLATION (nothing matched) is idempotent; WF routes it to EXIT without error
    - released_count bound from updated_count (number of records actually reverted)
```
