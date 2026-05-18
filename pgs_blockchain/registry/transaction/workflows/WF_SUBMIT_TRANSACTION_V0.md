# WF_SUBMIT_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** WF_SUBMIT_TRANSACTION_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_TRANSACTION_SUBMITTED_V0, CC_RESOLVE_ACTOR_ID_V0, CC_VALIDATE_TX_STRUCTURE_V0, CC_VALIDATE_TX_POLICY_V0, CC_RESERVE_NONCE_V0, CC_BUILD_ETH_TX_V0, CC_SIGN_TRANSACTION_V0, CC_HASH_TRANSACTION_V0, CC_PERSIST_MEMPOOL_TX_V0, CC_APPEND_TX_EVENT_V0

---

## 1. Intent

Submit an ETH transaction: validate structure and policy, reserve nonce, build unsigned transaction, sign, hash, persist to mempool, and emit lifecycle event.

---

## 2. Rationale

Transaction submission requires:
- Actor resolution (verified identity)
- Structural validation of transaction fields
- Policy validation (wallet ownership, EOA capability)
- Atomic nonce reservation
- EIP-1559 transaction building
- ECDSA signing with re-derived keys
- Keccak-256 hashing of signed transaction
- Append-only mempool persistence
- Lifecycle event emission

All failure paths exit immediately. No partial side-effects — signing must complete before persistence.

---

## 3. Execution Graph

```
IN_TRANSACTION_SUBMITTED_V0
    ├─ ACK → CC_RESOLVE_ACTOR_ID_V0
    │         ├─ SUCCESS → CC_VALIDATE_TX_STRUCTURE_V0
    │         │             ├─ SUCCESS → CC_VALIDATE_TX_POLICY_V0
    │         │             │             ├─ SUCCESS → CC_RESERVE_NONCE_V0
    │         │             │             │             ├─ SUCCESS → CC_BUILD_ETH_TX_V0
    │         │             │             │             │             ├─ SUCCESS → CC_SIGN_TRANSACTION_V0
    │         │             │             │             │             │             ├─ SUCCESS → CC_HASH_TRANSACTION_V0
    │         │             │             │             │             │             │             ├─ SUCCESS → CC_PERSIST_MEMPOOL_TX_V0
    │         │             │             │             │             │             │             │             ├─ SUCCESS → CC_APPEND_TX_EVENT_V0
    │         │             │             │             │             │             │             │             │             ├─ SUCCESS → EXIT_SUCCESS
    │         │             │             │             │             │             │             │             │             └─ * → EXIT
    │         │             │             │             │             │             │             │             ├─ ALREADY_EXISTS → EXIT_DUPLICATE
    │         │             │             │             │             │             │             │             └─ * → EXIT
    │         │             │             │             │             │             │             └─ * → EXIT
    │         │             │             │             │             │             └─ * → EXIT
    │         │             │             │             │             └─ * → EXIT
    │         │             │             │             └─ * → EXIT
    │         │             │             └─ * → EXIT
    │         │             └─ * → EXIT
    │         └─ * → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_TRANSACTION_SUBMITTED_V0 | IN | Entry intent for transaction submission |
| CC_RESOLVE_ACTOR_ID_V0 | CC | Resolve actor by natural keys |
| CC_VALIDATE_TX_STRUCTURE_V0 | CC | Validate transaction field types and formats |
| CC_VALIDATE_TX_POLICY_V0 | CC | Validate wallet ownership and tx capability |
| CC_RESERVE_NONCE_V0 | CC | Atomically reserve transaction nonce |
| CC_BUILD_ETH_TX_V0 | CC | Generate tx_id and build unsigned EIP-1559 bytes |
| CC_SIGN_TRANSACTION_V0 | CC | Re-derive key and sign transaction |
| CC_HASH_TRANSACTION_V0 | CC | Compute keccak-256 hash of signed transaction |
| CC_PERSIST_MEMPOOL_TX_V0 | CC | Persist to mempool and register in tx index |
| CC_APPEND_TX_EVENT_V0 | CC | Emit transaction lifecycle event |
| EXIT_SUCCESS | EXIT | Successful completion |
| EXIT_DUPLICATE | EXIT | Duplicate nonce rejection |
| EXIT | EXIT | Failure exit |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | EV_WALLET_CREATED_V0 |

Wallet must exist before transaction submission.

---

## Machine

```yaml
wf_code: WF_SUBMIT_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_SUBMIT_TRANSACTION_V0

core:
  runtime_binding: blockchain::RB_SUBMIT_TRANSACTION_V0
  summary: Submit ETH transaction — validate, sign, persist to mempool

  admission:
    requires:
      - EV_WALLET_CREATED_V0
    forbids: []
    bindings:
      EV_WALLET_CREATED_V0:
        wallet_id: wallet_id

  start_node: IN_TRANSACTION_SUBMITTED_V0

  nodes:
    IN_TRANSACTION_SUBMITTED_V0:
      type: IN
      code: IN_TRANSACTION_SUBMITTED_V0
      next:
        ACK: CC_RESOLVE_ACTOR_ID_V0
        NACK: EXIT

    CC_RESOLVE_ACTOR_ID_V0:
      type: CC
      code: CC_RESOLVE_ACTOR_ID_V0
      inputs:
        actor_record: $.payload.actor_record
      next:
        SUCCESS: CC_VALIDATE_TX_STRUCTURE_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_VALIDATE_TX_STRUCTURE_V0:
      type: CC
      code: CC_VALIDATE_TX_STRUCTURE_V0
      inputs:
        to_address: $.payload.to_address
        value: $.payload.value
        gas_limit: $.payload.gas_limit
        max_fee_per_gas: $.payload.max_fee_per_gas
        max_priority_fee_per_gas: $.payload.max_priority_fee_per_gas
        data: $.payload.data
      next:
        SUCCESS: CC_VALIDATE_TX_POLICY_V0
        VIOLATION: EXIT

    CC_VALIDATE_TX_POLICY_V0:
      type: CC
      code: CC_VALIDATE_TX_POLICY_V0
      inputs:
        wallet_id: $.payload.wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        value: $.payload.value
        tx_type: ETH
      next:
        SUCCESS: CC_RESERVE_NONCE_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_RESERVE_NONCE_V0:
      type: CC
      code: CC_RESERVE_NONCE_V0
      inputs:
        wallet_id: $.payload.wallet_id
        wallet_record: $.results.CC_VALIDATE_TX_POLICY_V0.wallet_record
      next:
        SUCCESS: CC_BUILD_ETH_TX_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_BUILD_ETH_TX_V0:
      type: CC
      code: CC_BUILD_ETH_TX_V0
      inputs:
        from_address: $.results.CC_VALIDATE_TX_POLICY_V0.from_address
        to_address: $.payload.to_address
        value: $.payload.value
        nonce: $.results.CC_RESERVE_NONCE_V0.nonce
        gas_limit: $.payload.gas_limit
        max_fee_per_gas: $.payload.max_fee_per_gas
        max_priority_fee_per_gas: $.payload.max_priority_fee_per_gas
        data: $.payload.data
        chain_id: 66
      next:
        SUCCESS: CC_SIGN_TRANSACTION_V0
        VIOLATION: EXIT

    CC_SIGN_TRANSACTION_V0:
      type: CC
      code: CC_SIGN_TRANSACTION_V0
      inputs:
        mnemonic: $.payload.mnemonic
        unsigned_tx_bytes: $.results.CC_BUILD_ETH_TX_V0.unsigned_tx_bytes
      next:
        SUCCESS: CC_HASH_TRANSACTION_V0
        VIOLATION: EXIT

    CC_HASH_TRANSACTION_V0:
      type: CC
      code: CC_HASH_TRANSACTION_V0
      inputs:
        signed_tx_bytes: $.results.CC_SIGN_TRANSACTION_V0.signed_tx_bytes
      next:
        SUCCESS: CC_PERSIST_MEMPOOL_TX_V0
        VIOLATION: EXIT

    CC_PERSIST_MEMPOOL_TX_V0:
      type: CC
      code: CC_PERSIST_MEMPOOL_TX_V0
      inputs:
        tx_id: $.results.CC_BUILD_ETH_TX_V0.tx_id
        tx_hash: $.results.CC_HASH_TRANSACTION_V0.tx_hash
        tx_type: ETH
        from_address: $.results.CC_VALIDATE_TX_POLICY_V0.from_address
        to_address: $.payload.to_address
        value: $.payload.value
        nonce: $.results.CC_RESERVE_NONCE_V0.nonce
        gas_limit: $.payload.gas_limit
        max_fee_per_gas: $.payload.max_fee_per_gas
        max_priority_fee_per_gas: $.payload.max_priority_fee_per_gas
        data: $.payload.data
        chain_id: 66
        signature: $.results.CC_SIGN_TRANSACTION_V0.signature
        wallet_id: $.payload.wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
      next:
        SUCCESS: CC_APPEND_TX_EVENT_V0
        ALREADY_EXISTS: EXIT_DUPLICATE
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_APPEND_TX_EVENT_V0:
      type: CC
      code: CC_APPEND_TX_EVENT_V0
      inputs:
        event_type: EV_TRANSACTION_SUBMITTED_V0
        tx_id: $.results.CC_BUILD_ETH_TX_V0.tx_id
        tx_hash: $.results.CC_HASH_TRANSACTION_V0.tx_hash
        wallet_id: $.payload.wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        data:
          from_address: $.results.CC_VALIDATE_TX_POLICY_V0.from_address
          to_address: $.payload.to_address
          value: $.payload.value
          status: PENDING
      next:
        SUCCESS: EXIT_SUCCESS
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT_SUCCESS:
      type: EXIT
      reason: COMPLETED

    EXIT_DUPLICATE:
      type: EXIT
      reason: DUPLICATE_NONCE

    EXIT:
      type: EXIT
      reason: EXITED
```
