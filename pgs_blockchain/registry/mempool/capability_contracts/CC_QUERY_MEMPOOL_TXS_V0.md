# CC_QUERY_MEMPOOL_TXS_V0

## Header (Mandatory)

- **Artifact Code:** CC_QUERY_MEMPOOL_TXS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_FILTER_RECORDS_V0

---

## 1. Intent

Query the MEMPOOL store for all pending transactions, returning their IDs for block assembly.

---

## 2. Rationale

Block proposal requires a list of pending transaction IDs to include. This CC is owned by the `mempool` subdomain — it reads from mempool-owned storage and exposes a clean cross-subdomain interface. The `consensus_pos` subdomain calls this CC but does not own or access the MEMPOOL store directly.

CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for an empty store (substrate invariant). CT_PURE_FILTER_RECORDS_V0 detects the empty case (no records with status=PENDING) and exits VIOLATION. WF_PROPOSE_BLOCK_V0 routes CC VIOLATION → CC_SKIP_ROUND_V0 — an empty mempool is a valid round-skip condition, not a protocol error.

Replaces CC_QUERY_PENDING_TRANSACTIONS_V0 (which queried the TRANSACTION store and leaked mempool state into the settled ledger domain).

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | LIST MEMPOOL store → all records and keys |
| 2 | CT_PURE_FILTER_RECORDS_V0 | CT | Assert status=PENDING present (VIOLATION if none) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| (none) | — | — | No inputs required; queries full MEMPOOL store |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_ids | array | List of pending transaction IDs (store keys from MEMPOOL) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | One or more pending transactions found; tx_ids populated |
| VIOLATION | No pending transactions in MEMPOOL (empty or no PENDING records) |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION (empty mempool) is routed by WF_PROPOSE_BLOCK_V0 → CC_SKIP_ROUND_V0 (valid skip condition)
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_QUERY_MEMPOOL_TXS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Query MEMPOOL store for pending transactions; return tx_ids for block assembly

  inputs: {}

  outputs:
    tx_ids:
      type: array
      items:
        type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: list_mempool_entries
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: MEMPOOL
      op: LIST
      inputs: {}
      outputs:
        mempool_records: $.capability_result.records
        tx_ids: $.capability_result.keys
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: assert_mempool_non_empty
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: assert_mempool_non_empty
      transform: capability_transforms::CT_PURE_FILTER_RECORDS_V0
      inputs:
        source: $.results.list_mempool_entries.mempool_records
        filter:
          status: PENDING
      outputs: {}
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: mempool
  notes:
    - Owned by blockchain::mempool; called cross-subdomain by WF_PROPOSE_BLOCK_V0 (consensus_pos)
    - Replaces CC_QUERY_PENDING_TRANSACTIONS_V0 — MEMPOOL store is the canonical pending tx source
    - CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for empty store (substrate invariant); NOT_FOUND not used for list
    - CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when no PENDING records found — covers empty mempool case
    - VIOLATION from this CC is routed by WF_PROPOSE_BLOCK_V0 → CC_SKIP_ROUND_V0 (no pending txs = valid skip)
    - tx_ids bound from list_mempool_entries.tx_ids (store keys = tx IDs); assert step validates non-empty
```
