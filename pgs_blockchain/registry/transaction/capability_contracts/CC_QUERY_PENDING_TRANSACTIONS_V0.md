# CC_QUERY_PENDING_TRANSACTIONS_V0

## Header (Mandatory)

- **Artifact Code:** CC_QUERY_PENDING_TRANSACTIONS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_FILTER_RECORDS_V0

---

## 1. Intent

Query the TRANSACTION store for all transactions with status=pending, returning their IDs for block assembly.

---

## 2. Rationale

Block proposal requires a list of pending transactions to include. This CC is owned by the `transaction` subdomain — it reads from transaction-owned storage and exposes a clean cross-subdomain interface. The consensus_pos subdomain calls this CC but does not own or access the TRANSACTION store directly.

CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for an empty store (substrate invariant). The CT_PURE_FILTER_RECORDS_V0 assert step detects the empty case (or no pending txs) and exits VIOLATION. WF_PROPOSE_BLOCK_V0 routes CC VIOLATION → CC_SKIP_ROUND_V0 (no pending transactions is a valid round-skip condition, not a protocol error).

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | LIST TRANSACTION store → all records |
| 2 | CT_PURE_FILTER_RECORDS_V0 | CT | Assert status=PENDING present (VIOLATION if none) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| filter | object | false | Optional filter parameters (default: status=pending) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_ids | array | Ordered list of pending transaction IDs |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | One or more pending transactions found; tx_ids populated |
| VIOLATION | No pending transactions found (CT filter found no PENDING records) or storage data malformed |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION from CT_PURE_FILTER_RECORDS_V0 (no PENDING records) is routed by WF_PROPOSE_BLOCK_V0 → CC_SKIP_ROUND_V0
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_QUERY_PENDING_TRANSACTIONS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Query TRANSACTION store for pending transactions

  inputs:
    filter:
      type: object
      required: false

  outputs:
    tx_ids:
      type: array
      items:
        type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: list_pending_transactions
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: TRANSACTION
      op: LIST
      inputs: {}
      outputs:
        tx_list: $.capability_result.records
        tx_ids: $.capability_result.keys
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: assert_pending_present
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: assert_pending_present
      transform: capability_transforms::CT_PURE_FILTER_RECORDS_V0
      inputs:
        source: $.results.list_pending_transactions.tx_list
        filter:
          status: PENDING
      outputs: {}
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: transaction
  notes:
    - Owned by blockchain::transaction; called cross-subdomain by WF_PROPOSE_BLOCK_V0
    - CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for empty store (substrate invariant)
    - CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when no PENDING records found — covers empty mempool case
    - VIOLATION from this CC is routed by WF_PROPOSE_BLOCK_V0 → CC_SKIP_ROUND_V0 (no pending txs = valid skip condition)
    - tx_ids bound from list_pending_transactions.tx_ids (store keys = tx IDs); assert step validates non-empty
```
