# CC_DRAIN_MEMPOOL_V0

## Header (Mandatory)

- **Artifact Code:** CC_DRAIN_MEMPOOL_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Delete a list of consumed transaction IDs from the MEMPOOL store after they have been included in a formed block.

---

## 2. Rationale

The MEMPOOL is an ephemeral staging buffer. Once transactions have been formed into a block (by CC_FORM_BLOCK_V0), they must be removed from the MEMPOOL before the consensus round is recorded. This CC owns the drain operation — it is idempotent (NOT_FOUND per tx_id is treated as already drained) and DELETE-only (it never writes to the TRANSACTION store or any other store).

Drain occurs after block formation and before round recording in WF_PROPOSE_BLOCK_V0, so the block_id provides the correlation reference.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | DELETE_MANY — remove all tx_ids from MEMPOOL store |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_ids | array | true | List of transaction IDs to delete from MEMPOOL |
| block_id | string | true | Block ID that consumed these transactions (correlation reference) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| drained_count | integer | Number of transactions actually removed from MEMPOOL |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Delete operation completed; drained_count reflects keys actually removed |
| VIOLATION | tx_ids input missing or malformed |
| BACKEND_ERROR | Storage write failure |

---

## 7. Failure Semantics

- NOT_FOUND per tx_id is treated as already drained — idempotent, not an error
- VIOLATION only if tx_ids is missing or not an array
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_DRAIN_MEMPOOL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Delete consumed transactions from MEMPOOL store after block formation

  inputs:
    tx_ids:
      type: array
      required: true
      description: Transaction IDs to remove from MEMPOOL
      items:
        type: string
    block_id:
      type: string
      required: true
      description: Block ID that consumed these transactions (correlation reference)

  outputs:
    drained_count:
      type: integer
      description: Number of keys actually removed from MEMPOOL

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: delete_consumed_txs
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: MEMPOOL
      op: DELETE_MANY
      inputs:
        keys: $.inputs.tx_ids
      outputs:
        drained_count: $.capability_result.drained_count
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

  error_codes:
    VIOLATION: TX_DRAIN_FAILED
    BACKEND_ERROR: TX_DRAIN_FAILED

extensions:
  subdomain: mempool
  notes:
    - DELETE-only operation; never writes to TRANSACTION store or any other store
    - Idempotent — NOT_FOUND per tx_id treated as already drained (DELETE_MANY substrate invariant)
    - Called by WF_PROPOSE_BLOCK_V0 after CC_FORM_BLOCK_V0 SUCCESS, before CC_RECORD_CONSENSUS_ROUND_V0
    - block_id is a correlation reference only; not written to any store by this CC
    - drained_count reflects keys actually present and removed; may be less than len(tx_ids) on partial re-drain
```
