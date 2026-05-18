# CC_PERSIST_MEMPOOL_TX_V0

## Header (Mandatory)

- **Artifact Code:** CC_PERSIST_MEMPOOL_TX_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0, CS_REGISTRY_V0

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
| 4 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_id | string | true | Transaction identifier |
| tx_hash | string | true | Transaction hash |
| tx_type | string | true | Transaction type (ETH) |
| from_address | string | true | Sender address |
| to_address | string | true | Destination address |
| value | string | true | Transfer value in wei |
| nonce | integer | true | Transaction nonce |
| gas_limit | integer | true | Gas limit |
| max_fee_per_gas | string | true | Max fee per gas |
| max_priority_fee_per_gas | string | true | Max priority fee |
| data | string | true | Transaction data |
| chain_id | integer | true | Chain identifier |
| signature | object | true | {v, r, s} signature |
| wallet_id | string | true | Source wallet |
| actor_id | string | true | Submitting actor |

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
    tx_hash:
      type: string
      required: true
    tx_type:
      type: string
      required: true
    from_address:
      type: string
      required: true
    to_address:
      type: string
      required: true
    value:
      type: string
      required: true
    nonce:
      type: integer
      required: true
    gas_limit:
      type: integer
      required: true
    max_fee_per_gas:
      type: string
      required: true
    max_priority_fee_per_gas:
      type: string
      required: true
    data:
      type: string
      required: true
    chain_id:
      type: integer
      required: true
    signature:
      type: object
      required: true
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_nonce_key
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: NONCE
        data:
          from_address: $.inputs.from_address
          nonce: $.inputs.nonce
      outputs:
        nonce_key: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: register_nonce
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.results.generate_nonce_key.nonce_key
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.from_address
        metadata:
          nonce: $.inputs.nonce
          wallet_id: $.inputs.wallet_id
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
          from_address: $.inputs.from_address
          to_address: $.inputs.to_address
          value: $.inputs.value
          nonce: $.inputs.nonce
          gas_limit: $.inputs.gas_limit
          max_fee_per_gas: $.inputs.max_fee_per_gas
          max_priority_fee_per_gas: $.inputs.max_priority_fee_per_gas
          data: $.inputs.data
          chain_id: $.inputs.chain_id
          signature: $.inputs.signature
          wallet_id: $.inputs.wallet_id
          actor_id: $.inputs.actor_id
          status: PENDING
          created_at: "{{timestamp}}"
      outputs:
        result_status: $.result_status
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
          wallet_id: $.inputs.wallet_id
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
