# CC_GENERATE_TX_ID_V0

## Header (Mandatory)

- **Artifact Code:** CC_GENERATE_TX_ID_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0

---

## 1. Intent

Generate a deterministic transaction ID and transaction hash from transaction data fields.

---

## 2. Rationale

BACHI transactions do not use ETH-style EIP-1559 signing or keccak-256 hashing. Instead, both
tx_id and tx_hash are content-addressable identifiers derived from the transaction's core data
using CT_PURE_GENERATE_ID_V0. This replaces CC_BUILD_ETH_TX_V0 + CC_HASH_TRANSACTION_V0 in the
BACHI-native transaction pipeline.

- tx_id: T-prefixed deterministic ID from transaction data
- tx_hash: T_HASH-prefixed deterministic ID from transaction data (same source data, different prefix)

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID (tx_id) |
| 2 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID (tx_hash) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_type | string | true | Transaction type (TRANSFER, STAKE, UNSTAKE, MINT, BURN, POOL, REWARD, SLASH) |
| from_wallet_id | string | false | Source wallet identifier (null for MINT, REWARD) |
| to_wallet_id | string | false | Destination wallet identifier (null for BURN, POOL) |
| amount | number | true | Transaction amount in BACHI |
| actor_id | string | false | Submitting actor identifier (null for SYSTEM transactions) |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_id | string | T-prefixed transaction identifier |
| tx_hash | string | T_HASH-prefixed transaction hash |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Both tx_id and tx_hash generated |
| VIOLATION | Invalid input |

---

## Machine

```yaml
cc_code: CC_GENERATE_TX_ID_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Generate deterministic tx_id and tx_hash for BACHI transactions

  inputs:
    tx_type:
      type: string
      required: true
      description: Transaction type
    from_wallet_id:
      type: string
      required: false
      description: Source wallet identifier (null for MINT, REWARD)
    to_wallet_id:
      type: string
      required: false
      description: Destination wallet identifier (null for BURN, POOL)
    amount:
      type: number
      required: true
      description: Transaction amount in BACHI
    actor_id:
      type: string
      required: false
      description: Submitting actor (null for SYSTEM transactions)

  outputs:
    tx_id:
      type: string
    tx_hash:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_tx_id
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: T
        data:
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          to_wallet_id: $.inputs.to_wallet_id
          amount: $.inputs.amount
          actor_id: $.inputs.actor_id
      outputs:
        tx_id: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: generate_tx_hash
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      op: GENERATE_ID
      inputs:
        prefix: T_HASH
        data:
          tx_type: $.inputs.tx_type
          from_wallet_id: $.inputs.from_wallet_id
          to_wallet_id: $.inputs.to_wallet_id
          amount: $.inputs.amount
          actor_id: $.inputs.actor_id
      outputs:
        tx_hash: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```
