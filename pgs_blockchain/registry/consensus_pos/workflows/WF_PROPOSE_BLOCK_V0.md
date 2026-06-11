# WF_PROPOSE_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** WF_PROPOSE_BLOCK_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** IN_BLOCK_PROPOSED_V0, CC_QUERY_ELIGIBLE_VALIDATORS_V0, CC_SELECT_PROPOSER_V0, CC_CLAIM_MEMPOOL_TXS_V0, CC_RELEASE_CLAIMED_MEMPOOL_V0, CC_FORM_BLOCK_V0, CC_DRAIN_MEMPOOL_V0, CC_RECORD_CONSENSUS_ROUND_V0, CC_SKIP_ROUND_V0

---

## 1. Intent

Execute a consensus proposer selection round: identify eligible validators, select the proposer deterministically, atomically claim pending transactions from the MEMPOOL (mutual exclusion against concurrent slot workers), form a block, drain the MEMPOOL, record the round, or skip the round if no transactions are pending. On block formation failure, release claimed transactions back to PENDING.

---

## 2. Rationale

Block proposal is a multi-path workflow with two terminal outcomes:

- **Block proposed**: eligible validators exist, proposer selected, transactions pending → block formed and round recorded
- **Round skipped**: no eligible validators OR no pending transactions → round skipped and recorded

Each path is governed by CC-declared outcome routing — no runtime branching logic. Cross-subdomain CC calls (CC_CLAIM_MEMPOOL_TXS_V0, CC_RELEASE_CLAIMED_MEMPOOL_V0, and CC_DRAIN_MEMPOOL_V0 from mempool subdomain, CC_FORM_BLOCK_V0 from block subdomain) are permitted at the WF level; the WF does not own those stores.

The proposer selection is deterministic (round_number modulo eligible validator count) via CT_PURE_SELECT_PROPOSER_V0, ensuring that all nodes converge on the same proposer for a given round.

---

## 3. Execution Graph

```
IN_BLOCK_PROPOSED_V0
    ├─ ACK → CC_QUERY_ELIGIBLE_VALIDATORS_V0
    │           ├─ SUCCESS → CC_SELECT_PROPOSER_V0
    │           │               ├─ SUCCESS → CC_CLAIM_MEMPOOL_TXS_V0
    │           │               │               ├─ SUCCESS → CC_FORM_BLOCK_V0
    │           │               │               │               ├─ SUCCESS → CC_DRAIN_MEMPOOL_V0
    │           │               │               │               │               ├─ SUCCESS → CC_RECORD_CONSENSUS_ROUND_V0 → EXIT
    │           │               │               │               │               └─ * → EXIT
    │           │               │               │               ├─ VIOLATION → CC_RELEASE_CLAIMED_MEMPOOL_V0 → EXIT
    │           │               │               │               └─ BACKEND_ERROR → CC_RELEASE_CLAIMED_MEMPOOL_V0 → EXIT
    │           │               │               ├─ VIOLATION → CC_SKIP_ROUND_V0 → EXIT  (no pending txs)
    │           │               │               └─ BACKEND_ERROR → EXIT
    │           │               └─ VIOLATION → EXIT
    │           ├─ VIOLATION → EXIT  (no eligible validators — round not recorded)
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_BLOCK_PROPOSED_V0 | IN | Entry intent — validates payload |
| CC_QUERY_ELIGIBLE_VALIDATORS_V0 | CC | Query VALIDATOR store for active validators with stake |
| CC_SELECT_PROPOSER_V0 | CC | Deterministic round-robin proposer selection |
| CC_CLAIM_MEMPOOL_TXS_V0 | CC | Atomically claim PENDING txs for this proposer; mutual exclusion via per-file lock (cross-subdomain: mempool) |
| CC_RELEASE_CLAIMED_MEMPOOL_V0 | CC | Release this proposer's CLAIMED txs back to PENDING on block failure (cross-subdomain: mempool) |
| CC_FORM_BLOCK_V0 | CC | Form block, write to BLOCKS, append to BLOCK_EVENTS (cross-subdomain: block) |
| CC_DRAIN_MEMPOOL_V0 | CC | Delete consumed transactions from MEMPOOL store (cross-subdomain: mempool) |
| CC_RECORD_CONSENSUS_ROUND_V0 | CC | Record the consensus round journal entry in CONSENSUS_ROUNDS |
| CC_SKIP_ROUND_V0 | CC | Record a skipped round in CONSENSUS_ROUNDS and CONSENSUS_EVENTS |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

Round number must be a non-negative integer. Triggered_by must be a valid actor_id string. Timestamp must be ISO 8601.

---

## Machine

```yaml
wf_code: WF_PROPOSE_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_PROPOSE_BLOCK_V0
subdomain: consensus_pos

core:
  summary: Execute a consensus proposer selection and block formation round
  start_node: IN_BLOCK_PROPOSED_V0

  nodes:
    IN_BLOCK_PROPOSED_V0:
      type: IN
      code: IN_BLOCK_PROPOSED_V0
      next:
        ACK: CC_QUERY_ELIGIBLE_VALIDATORS_V0
        NACK: EXIT

    CC_QUERY_ELIGIBLE_VALIDATORS_V0:
      type: CC
      code: CC_QUERY_ELIGIBLE_VALIDATORS_V0
      inputs: {}
      next:
        SUCCESS: CC_SELECT_PROPOSER_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_SELECT_PROPOSER_V0:
      type: CC
      code: CC_SELECT_PROPOSER_V0
      inputs:
        eligible_validators: $.results.CC_QUERY_ELIGIBLE_VALIDATORS_V0.eligible_validators
        round_number: $.payload.round_number
      next:
        SUCCESS: CC_CLAIM_MEMPOOL_TXS_V0
        VIOLATION: EXIT

    CC_CLAIM_MEMPOOL_TXS_V0:
      type: CC
      code: CC_CLAIM_MEMPOOL_TXS_V0
      inputs:
        proposer_id: $.results.CC_SELECT_PROPOSER_V0.proposer_id
      next:
        SUCCESS: CC_FORM_BLOCK_V0
        VIOLATION: CC_SKIP_ROUND_V0
        BACKEND_ERROR: EXIT

    CC_FORM_BLOCK_V0:
      type: CC
      code: CC_FORM_BLOCK_V0
      inputs:
        round_id: $.payload.round_number
        proposer_id: $.results.CC_SELECT_PROPOSER_V0.proposer_id
        tx_ids: $.results.CC_CLAIM_MEMPOOL_TXS_V0.tx_ids
        timestamp: $.payload.timestamp
        slot: $.payload.slot
        epoch: $.payload.epoch
      next:
        SUCCESS: CC_DRAIN_MEMPOOL_V0
        VIOLATION: CC_RELEASE_CLAIMED_MEMPOOL_V0
        BACKEND_ERROR: CC_RELEASE_CLAIMED_MEMPOOL_V0

    CC_RELEASE_CLAIMED_MEMPOOL_V0:
      type: CC
      code: CC_RELEASE_CLAIMED_MEMPOOL_V0
      inputs:
        proposer_id: $.results.CC_SELECT_PROPOSER_V0.proposer_id
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_DRAIN_MEMPOOL_V0:
      type: CC
      code: CC_DRAIN_MEMPOOL_V0
      inputs:
        tx_ids: $.results.CC_CLAIM_MEMPOOL_TXS_V0.tx_ids
        block_id: $.results.CC_FORM_BLOCK_V0.block_id
      next:
        SUCCESS: CC_RECORD_CONSENSUS_ROUND_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_RECORD_CONSENSUS_ROUND_V0:
      type: CC
      code: CC_RECORD_CONSENSUS_ROUND_V0
      inputs:
        round_id: $.payload.round_number
        proposer_id: $.results.CC_SELECT_PROPOSER_V0.proposer_id
        block_id: $.results.CC_FORM_BLOCK_V0.block_id
        timestamp: $.payload.timestamp
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_SKIP_ROUND_V0:
      type: CC
      code: CC_SKIP_ROUND_V0
      inputs:
        round_id: $.payload.round_number
        proposer_id: $.results.CC_SELECT_PROPOSER_V0.proposer_id
        timestamp: $.payload.timestamp
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED

extensions:
  subdomain: consensus_pos
  notes:
    - CC_CLAIM_MEMPOOL_TXS_V0 replaces CC_QUERY_MEMPOOL_TXS_V0 in this WF — atomic claim prevents concurrent slot workers from double-including the same tx
    - CC_CLAIM_MEMPOOL_TXS_V0 and CC_DRAIN_MEMPOOL_V0 are owned by mempool subdomain (cross-subdomain calls)
    - CC_RELEASE_CLAIMED_MEMPOOL_V0 is the recovery path — reverts CLAIMED → PENDING on CC_FORM_BLOCK_V0 failure; scoped to this proposer_id
    - CC_FORM_BLOCK_V0 is owned by block subdomain (cross-subdomain call)
    - VIOLATION from CC_QUERY_ELIGIBLE_VALIDATORS_V0 exits immediately (no eligible validators — valid during bootstrap; no round record written)
    - VIOLATION from CC_CLAIM_MEMPOOL_TXS_V0 routes to CC_SKIP_ROUND_V0 (valid: proposer selected but no PENDING txs in MEMPOOL)
    - CC_SKIP_ROUND_V0 always receives a valid proposer_id (CC_SELECT_PROPOSER_V0 has completed on this path)
    - CC_DRAIN_MEMPOOL_V0 receives tx_ids from CC_CLAIM_MEMPOOL_TXS_V0 — the same IDs that were claimed and included in the formed block
    - CC_RELEASE_CLAIMED_MEMPOOL_V0 VIOLATION (nothing to release) routes to EXIT — idempotent, not an error
    - tx lifecycle: PENDING → CLAIMED (claim) → deleted from MEMPOOL + written to TRANSACTION store (drain+confirm) OR CLAIMED → PENDING (release on failure)
```
