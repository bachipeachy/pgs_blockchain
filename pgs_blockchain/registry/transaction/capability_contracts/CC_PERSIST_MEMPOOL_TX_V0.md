# CC_PERSIST_MEMPOOL_TX_V0

## Header (Mandatory)

- **Artifact Code:** CC_PERSIST_MEMPOOL_TX_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0

---

## 1. Intent

Persist the signed transaction to the local mempool and register in the transaction index.

---

## 2. Rationale

Only signed transactions are persisted. The mempool is append-only and immutable.
The transaction index maps tx_id → tx_hash for lookup. Record contains actor_id
and wallet_id only — no PII.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |
| 2 | CS_REGISTRY_V0 | CS | REGISTER |
| 3 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |
| 4 | CS_MUTABLE_JSON_V0 | CS | WRITE (pending tx record → MEMPOOL store) |
| 5 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_id | string | true | Transaction identifier (TX-prefixed, generated upstream) |
| tx_hash | string | true | Transaction hash (TX-prefixed, generated upstream) |
| tx_type | string | true | Transaction type — injected as wf_literal by each typed WF |
| from_wallet_id | string | false | Source wallet (null for MINT, REWARD) |
| to_wallet_id | string | false | Destination wallet (null for BURN, POOL) |
| amount | number | true | Transaction amount in BACHI |
| actor_id | string | false | Submitting actor (null for SYSTEM transactions) |
| gas_limit | integer | false | Gas limit (ENDUSER transactions only) |
| max_fee_per_gas | string | false | Max fee per gas (ENDUSER transactions only) |
| max_priority_fee_per_gas | string | false | Max priority fee per gas (ENDUSER transactions only) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | SUCCESS, VIOLATION, ALREADY_EXISTS, or BACKEND_ERROR |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Record persisted and indexed |
| ALREADY_EXISTS | Duplicate nonce for wallet (TX_NONCE_DUPLICATE) |
| VIOLATION | Duplicate tx_id or tx_hash (TX_PERSIST_FAILED) |
| BACKEND_ERROR | Storage write failure |

---

## Machine

```yaml
cc_code: CC_PERSIST_MEMPOOL_TX_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Persist signed transaction to mempool and register in index

  inputs:
    tx_id:
      type: string
      required: true
      description: Transaction identifier (T-prefixed)
    tx_hash:
      type: string
      required: true
      description: Transaction hash (T_HASH-prefixed)
    tx_type:
      type: string
      required: true
      description: Transaction type; injected as wf_literal by each typed WF
    from_wallet_id:
      type: string
      required: false
      description: Source wallet (null for MINT, REWARD)
    to_wallet_id:
      type: string
      required: false
      description: Destination wallet (null for BURN, POOL)
    amount:
      type: number
      required: true
      description: Transaction amount in BACHI
    actor_id:
      type: string
      required: false
      description: Submitting actor (null for SYSTEM transactions)
    gas_limit:
      type: integer
      required: false
    max_fee_per_gas:
      type: string
      required: false
    max_priority_fee_per_gas:
      type: string
      required: false

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_tx_key
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: T_KEY
        data:
          tx_id: $.inputs.tx_id
          tx_type: $.inputs.tx_type
      outputs:
        tx_key: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: register_tx_key
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.results.generate_tx_key.tx_key
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.tx_id
        metadata:
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          to_wallet_id: $.inputs.to_wallet_id
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: append_mempool_tx
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: TRANSACTION_EVENTS
      op: APPEND
      inputs:
        stream_id: $.inputs.tx_id
        actor_id: $.inputs.actor_id
        record:
          tx_id: $.inputs.tx_id
          tx_hash: $.inputs.tx_hash
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          to_wallet_id: $.inputs.to_wallet_id
          amount: $.inputs.amount
          actor_id: $.inputs.actor_id
          gas_limit: $.inputs.gas_limit
          max_fee_per_gas: $.inputs.max_fee_per_gas
          max_priority_fee_per_gas: $.inputs.max_priority_fee_per_gas
          status: PENDING
          created_at: "{{timestamp}}"
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: write_pending_tx
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: MEMPOOL
      op: WRITE
      inputs:
        key: $.inputs.tx_id
        value:
          tx_id: $.inputs.tx_id
          tx_hash: $.inputs.tx_hash
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          to_wallet_id: $.inputs.to_wallet_id
          amount: $.inputs.amount
          actor_id: $.inputs.actor_id
          status: PENDING
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: register_tx_hash
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.inputs.tx_id
        target_cs: capability_side_effects::CS_APPENDONLY_JSONL_V0
        target_ref: $.inputs.tx_hash
        metadata:
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          status: PENDING
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

  error_codes:
    ALREADY_EXISTS: TX_NONCE_DUPLICATE
    VIOLATION: TX_PERSIST_FAILED
    BACKEND_ERROR: TX_PERSIST_FAILED
```
