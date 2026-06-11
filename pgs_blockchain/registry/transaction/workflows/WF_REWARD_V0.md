# WF_REWARD_V0

## Header (Mandatory)

- **Artifact Code:** WF_REWARD_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_REWARD_V0, CC_VALIDATE_REWARD_POLICY_V0, CC_GENERATE_TX_ID_V0, CC_WRITE_MEMPOOL_TX_V0, CC_APPEND_TX_EVENT_V0

---

## 1. Intent

Submit a REWARD transaction: validate destination wallet existence, generate transaction IDs, persist to mempool, and emit lifecycle event.

---

## 2. Rationale

REWARD is a SYSTEM operation triggered by block finalization. No actor identity required. The source (POOL wallet) is auto-resolved. The destination wallet and block reference are declared. The BACHI model removes ETH signing.

---

## 3. Execution Graph

```
IN_REWARD_V0
    ├─ ACK → CC_VALIDATE_REWARD_POLICY_V0
    │         ├─ SUCCESS → CC_GENERATE_TX_ID_V0
    │         │             ├─ SUCCESS → CC_WRITE_MEMPOOL_TX_V0
    │         │             │             ├─ SUCCESS → CC_APPEND_TX_EVENT_V0
    │         │             │             │             ├─ SUCCESS → EXIT_SUCCESS
    │         │             │             │             └─ * → EXIT
    │         │             │             ├─ ALREADY_EXISTS → EXIT_DUPLICATE
    │         │             │             └─ * → EXIT
    │         │             └─ VIOLATION → EXIT
    │         ├─ NOT_FOUND → EXIT
    │         └─ * → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_REWARD_V0 | IN | Entry intent for REWARD |
| CC_VALIDATE_REWARD_POLICY_V0 | CC | Validate destination wallet existence (SYSTEM) |
| CC_GENERATE_TX_ID_V0 | CC | Generate deterministic tx_id and tx_hash |
| CC_WRITE_MEMPOOL_TX_V0 | CC | Write transaction to MEMPOOL store and register identity keys |
| CC_APPEND_TX_EVENT_V0 | CC | Emit transaction lifecycle event |
| EXIT_SUCCESS | EXIT | Successful completion |
| EXIT_DUPLICATE | EXIT | Duplicate transaction |
| EXIT | EXIT | Failure exit |

---

## 5. Admission

No actor admission required — SYSTEM authority.

---

## Machine

```yaml
wf_code: WF_REWARD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_REWARD_V0
subdomain: transaction

core:
  runtime_binding: blockchain::RB_REWARD_V0
  summary: Submit REWARD transaction (SYSTEM) — validate destination wallet, persist to mempool

  admission:
    requires: []
    forbids: []

  start_node: IN_REWARD_V0

  nodes:
    IN_REWARD_V0:
      type: IN
      code: IN_REWARD_V0
      next:
        ACK: CC_VALIDATE_REWARD_POLICY_V0
        NACK: EXIT

    CC_VALIDATE_REWARD_POLICY_V0:
      type: CC
      code: CC_VALIDATE_REWARD_POLICY_V0
      inputs:
        triggered_by: $.payload.triggered_by
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
        block_hash: $.payload.block_hash
      next:
        SUCCESS: CC_GENERATE_TX_ID_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_GENERATE_TX_ID_V0:
      type: CC
      code: CC_GENERATE_TX_ID_V0
      inputs:
        tx_type: REWARD
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
      next:
        SUCCESS: CC_WRITE_MEMPOOL_TX_V0
        VIOLATION: EXIT

    CC_WRITE_MEMPOOL_TX_V0:
      type: CC
      code: CC_WRITE_MEMPOOL_TX_V0
      inputs:
        tx_id: $.results.CC_GENERATE_TX_ID_V0.tx_id
        tx_hash: $.results.CC_GENERATE_TX_ID_V0.tx_hash
        tx_type: REWARD
        to_wallet_id: $.payload.to_wallet_id
        amount: $.payload.amount
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
        actor_id: SYSTEM
        data:
          tx_type: REWARD
          to_wallet_id: $.payload.to_wallet_id
          amount: $.payload.amount
          block_hash: $.payload.block_hash
          triggered_by: $.payload.triggered_by
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
