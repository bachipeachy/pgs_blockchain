# WF_UNSTAKE_V0

## Header (Mandatory)

- **Artifact Code:** WF_UNSTAKE_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_UNSTAKE_V0, CC_RESOLVE_ACTOR_ID_V0, CC_VALIDATE_UNSTAKE_POLICY_V0, CC_GENERATE_TX_ID_V0, CC_WRITE_MEMPOOL_TX_V0, CC_APPEND_TX_EVENT_V0

---

## 1. Intent

Submit an UNSTAKE transaction: validate actor identity and destination wallet ownership, generate transaction IDs, persist to mempool, and emit lifecycle event.

---

## 2. Rationale

UNSTAKE is an ENDUSER operation. The actor withdraws their staked BACHI to their own wallet. The source (POOL wallet) is auto-resolved by CC_VALIDATE_UNSTAKE_POLICY_V0 — not supplied by the caller. The BACHI model removes ETH signing.

---

## 3. Execution Graph

```
IN_UNSTAKE_V0
    ├─ ACK → CC_RESOLVE_ACTOR_ID_V0
    │         ├─ SUCCESS → CC_VALIDATE_UNSTAKE_POLICY_V0
    │         │             ├─ SUCCESS → CC_GENERATE_TX_ID_V0
    │         │             │             ├─ SUCCESS → CC_WRITE_MEMPOOL_TX_V0
    │         │             │             │             ├─ SUCCESS → CC_APPEND_TX_EVENT_V0
    │         │             │             │             │             ├─ SUCCESS → EXIT_SUCCESS
    │         │             │             │             │             └─ * → EXIT
    │         │             │             │             ├─ ALREADY_EXISTS → EXIT_DUPLICATE
    │         │             │             │             └─ * → EXIT
    │         │             │             └─ VIOLATION → EXIT
    │         │             ├─ NOT_FOUND → EXIT
    │         │             └─ * → EXIT
    │         └─ * → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_UNSTAKE_V0 | IN | Entry intent for UNSTAKE |
| CC_RESOLVE_ACTOR_ID_V0 | CC | Resolve actor from actor_record |
| CC_VALIDATE_UNSTAKE_POLICY_V0 | CC | Validate to_wallet ownership by actor |
| CC_GENERATE_TX_ID_V0 | CC | Generate deterministic tx_id and tx_hash |
| CC_WRITE_MEMPOOL_TX_V0 | CC | Write transaction to MEMPOOL store and register identity keys |
| CC_APPEND_TX_EVENT_V0 | CC | Emit transaction lifecycle event |
| EXIT_SUCCESS | EXIT | Successful completion |
| EXIT_DUPLICATE | EXIT | Duplicate transaction |
| EXIT | EXIT | Failure exit |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | EV_WALLET_CREATED_V0 |

Actor wallet must exist before unstaking.

---

## Machine

```yaml
wf_code: WF_UNSTAKE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_UNSTAKE_V0
subdomain: transaction

core:
  runtime_binding: blockchain::RB_UNSTAKE_V0
  summary: Submit UNSTAKE transaction — validate actor ownership, persist to mempool

  admission:
    requires:
      - EV_WALLET_CREATED_V0
    forbids: []
    bindings:
      EV_WALLET_CREATED_V0:
        wallet_id: to_wallet_id

  start_node: IN_UNSTAKE_V0

  nodes:
    IN_UNSTAKE_V0:
      type: IN
      code: IN_UNSTAKE_V0
      next:
        ACK: CC_RESOLVE_ACTOR_ID_V0
        NACK: EXIT

    CC_RESOLVE_ACTOR_ID_V0:
      type: CC
      code: CC_RESOLVE_ACTOR_ID_V0
      inputs:
        actor_record: $.payload.actor_record
      next:
        SUCCESS: CC_VALIDATE_UNSTAKE_POLICY_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_VALIDATE_UNSTAKE_POLICY_V0:
      type: CC
      code: CC_VALIDATE_UNSTAKE_POLICY_V0
      inputs:
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        validator_index: $.payload.validator_index
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
      next:
        SUCCESS: CC_GENERATE_TX_ID_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_GENERATE_TX_ID_V0:
      type: CC
      code: CC_GENERATE_TX_ID_V0
      inputs:
        tx_type: UNSTAKE
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
      next:
        SUCCESS: CC_WRITE_MEMPOOL_TX_V0
        VIOLATION: EXIT

    CC_WRITE_MEMPOOL_TX_V0:
      type: CC
      code: CC_WRITE_MEMPOOL_TX_V0
      inputs:
        tx_id: $.results.CC_GENERATE_TX_ID_V0.tx_id
        tx_hash: $.results.CC_GENERATE_TX_ID_V0.tx_hash
        tx_type: UNSTAKE
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        gas_limit: $.payload.gas_limit
        max_fee_per_gas: $.payload.max_fee_per_gas
        max_priority_fee_per_gas: $.payload.max_priority_fee_per_gas
        created_at: "{{timestamp}}"
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
        tx_id: $.results.CC_GENERATE_TX_ID_V0.tx_id
        tx_hash: $.results.CC_GENERATE_TX_ID_V0.tx_hash
        wallet_id: $.payload.to_wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        data:
          tx_type: UNSTAKE
          to_wallet_id: $.payload.to_wallet_id
          validator_index: $.payload.validator_index
          amount: $.payload.amount
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
