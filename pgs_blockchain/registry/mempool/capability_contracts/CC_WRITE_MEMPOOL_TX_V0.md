# CC_WRITE_MEMPOOL_TX_V0

## Header (Mandatory)

- **Artifact Code:** CC_WRITE_MEMPOOL_TX_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** CC_PERSIST_MEMPOOL_TX_V0
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CS_REGISTRY_V0, CS_MUTABLE_JSON_V0

---

## 1. Intent

Write a signed transaction to the MEMPOOL staging buffer and register its identity keys in MEMPOOL_INDEX to enforce tx_id and tx_hash uniqueness.

---

## 2. Rationale

Mempool persistence is now scoped to the `mempool` subdomain — all reads and writes target MEMPOOL and MEMPOOL_INDEX stores exclusively, not the TRANSACTION store. This decouples pending transaction staging from the settled transaction ledger.

Deduplication is enforced by attempting to REGISTER both a composite mempool key (derived from tx_id + tx_type) and the tx_hash in MEMPOOL_INDEX before writing. REGISTER returns ALREADY_EXISTS directly, which routes the CC pipeline cleanly without a separate EXISTS check.

ETH-specific metadata fields (nonce, gas_limit, signature, etc.) are stored alongside the core record in MEMPOOL for downstream use during block formation.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID — derive composite mempool key from tx_id + tx_type |
| 2 | CS_REGISTRY_V0 | CS | REGISTER mempool_key → MEMPOOL_INDEX (tx_id dedup guard) |
| 3 | CS_MUTABLE_JSON_V0 | CS | WRITE full record keyed by tx_id → MEMPOOL store |
| 4 | CS_REGISTRY_V0 | CS | REGISTER tx_hash → MEMPOOL_INDEX (hash dedup guard) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_id | string | true | Transaction identifier (TX-prefixed, generated upstream) |
| tx_hash | string | true | Transaction hash (TX_HASH-prefixed, generated upstream) |
| tx_type | string | true | Transaction type — injected as wf_literal by each typed WF |
| actor_id | string | false | Submitting actor (null for SYSTEM transactions) |
| from_wallet_id | string | false | Source wallet address (null for MINT, REWARD) |
| to_wallet_id | string | false | Destination wallet address (null for BURN, POOL) |
| amount | number | true | Transaction amount in BACHI |
| created_at | string | true | Transaction creation timestamp (ISO 8601) |
| wallet_id | string | false | Internal wallet identifier |
| nonce | integer | false | Reserved transaction nonce (ETH-specific) |
| gas_limit | integer | false | Gas limit (ETH-specific) |
| max_fee_per_gas | string | false | Max fee per gas (ETH EIP-1559) |
| max_priority_fee_per_gas | string | false | Max priority fee per gas (ETH EIP-1559) |
| data | string | false | Calldata payload (ETH-specific) |
| chain_id | integer | false | Chain identifier (ETH-specific) |
| signature | string | false | ECDSA signature bytes (ETH-specific) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | SUCCESS, VIOLATION, ALREADY_EXISTS, or BACKEND_ERROR |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Record written to MEMPOOL; both keys registered in MEMPOOL_INDEX |
| ALREADY_EXISTS | Duplicate tx_id or tx_hash (mempool dedup guard fired) |
| VIOLATION | Key generation failed or registry key validation failed |
| BACKEND_ERROR | Storage write or registry write failure |

---

## Machine

```yaml
cc_code: CC_WRITE_MEMPOOL_TX_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Write signed transaction to MEMPOOL and register identity keys in MEMPOOL_INDEX

  inputs:
    tx_id:
      type: string
      required: true
      description: Transaction identifier (TX-prefixed)
    tx_hash:
      type: string
      required: true
      description: Transaction hash (TX_HASH-prefixed)
    tx_type:
      type: string
      required: true
      description: Transaction type; injected as wf_literal by each typed WF
    actor_id:
      type: string
      required: false
      description: Submitting actor (null for SYSTEM transactions)
    from_wallet_id:
      type: string
      required: false
      description: Source wallet address (null for MINT, REWARD)
    to_wallet_id:
      type: string
      required: false
      description: Destination wallet address (null for BURN, POOL)
    amount:
      type: number
      required: true
      description: Transaction amount in BACHI
    created_at:
      type: string
      required: true
      description: Transaction creation timestamp (ISO 8601)
    wallet_id:
      type: string
      required: false
    nonce:
      type: integer
      required: false
    gas_limit:
      type: integer
      required: false
    max_fee_per_gas:
      type: string
      required: false
    max_priority_fee_per_gas:
      type: string
      required: false
    data:
      type: string
      required: false
    chain_id:
      type: integer
      required: false
    signature:
      type: string
      required: false

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_mempool_key
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: M_KEY
        data:
          tx_id: $.inputs.tx_id
          tx_type: $.inputs.tx_type
      outputs:
        mempool_key: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: register_tx_id
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: MEMPOOL_INDEX
      op: REGISTER
      inputs:
        key: $.results.generate_mempool_key.mempool_key
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.tx_id
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        ALREADY_EXISTS: exit
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
          wallet_id: $.inputs.wallet_id
          status: PENDING
          created_at: $.inputs.created_at
          arrived_at: "{{timestamp}}"
          nonce: $.inputs.nonce
          gas_limit: $.inputs.gas_limit
          max_fee_per_gas: $.inputs.max_fee_per_gas
          max_priority_fee_per_gas: $.inputs.max_priority_fee_per_gas
          data: $.inputs.data
          chain_id: $.inputs.chain_id
          signature: $.inputs.signature
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: register_tx_hash
      side_effect: capability_side_effects::CS_REGISTRY_V0
      store: MEMPOOL_INDEX
      op: REGISTER
      inputs:
        key: $.inputs.tx_hash
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.tx_id
      outputs:
        result_status: $.result_status
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

  error_codes:
    ALREADY_EXISTS: TX_MEMPOOL_DUPLICATE
    VIOLATION: TX_MEMPOOL_WRITE_FAILED
    BACKEND_ERROR: TX_MEMPOOL_WRITE_FAILED

extensions:
  subdomain: mempool
  notes:
    - Supersedes CC_PERSIST_MEMPOOL_TX_V0; all writes go to MEMPOOL store, not TRANSACTION store
    - MEMPOOL_INDEX stores both mempool_key (tx_id+tx_type composite) and tx_hash as registry keys
    - REGISTER used for dedup — returns ALREADY_EXISTS directly without a separate EXISTS check
    - ETH metadata fields (nonce, gas_limit, signature, etc.) stored in MEMPOOL record for block formation use
    - arrived_at is the mempool ingestion timestamp; created_at is the transaction creation time from upstream
```
