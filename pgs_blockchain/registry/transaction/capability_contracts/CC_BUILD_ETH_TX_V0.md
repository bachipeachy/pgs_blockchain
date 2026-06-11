# CC_BUILD_ETH_TX_V0

## Header (Mandatory)

- **Artifact Code:** CC_BUILD_ETH_TX_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** RETIRED
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CT_PURE_BUILD_ETH_TRANSACTION_V0

---

## 1. Intent

Generate a deterministic transaction ID and build the unsigned EIP-1559 transaction bytes.

---

## 2. Rationale

Transaction ID generation and unsigned byte encoding are separated from signing
to maintain the invariant that unsigned material is never persisted. The tx_id
is content-addressed from transaction fields.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | GENERATE_ID |
| 2 | CT_PURE_BUILD_ETH_TRANSACTION_V0 | CT | BUILD_ETH_TRANSACTION |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| from_address | string | true | Sender address |
| to_address | string | true | Destination address |
| value | string | true | Transfer value in wei |
| nonce | integer | true | Reserved nonce |
| gas_limit | integer | false | Gas limit |
| max_fee_per_gas | string | false | Max fee per gas |
| max_priority_fee_per_gas | string | false | Max priority fee |
| data | string | false | Transaction data |
| chain_id | integer | true | Chain identifier |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| tx_id | string | Deterministic transaction identifier |
| unsigned_tx_bytes | string | RLP-encoded EIP-1559 unsigned transaction hex |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | ID generated and transaction encoded |
| VIOLATION | Invalid inputs or encoding failure |

---

## Machine

```yaml
cc_code: CC_BUILD_ETH_TX_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Generate tx_id and build unsigned EIP-1559 transaction

  inputs:
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
      required: true

  outputs:
    tx_id:
      type: string
    unsigned_tx_bytes:
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
          from_address: $.inputs.from_address
          to_address: $.inputs.to_address
          value: $.inputs.value
          nonce: $.inputs.nonce
          chain_id: $.inputs.chain_id
      outputs:
        tx_id: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: continue
        VIOLATION: exit

    - step: build_eth_transaction
      transform: blockchain::CT_PURE_BUILD_ETH_TRANSACTION_V0
      op: BUILD_ETH_TRANSACTION
      inputs:
        chain_id: $.inputs.chain_id
        nonce: $.inputs.nonce
        max_priority_fee_per_gas: $.inputs.max_priority_fee_per_gas
        max_fee_per_gas: $.inputs.max_fee_per_gas
        gas_limit: $.inputs.gas_limit
        to: $.inputs.to_address
        value: $.inputs.value
        data: $.inputs.data
      outputs:
        unsigned_tx_bytes: $.capability_result.unsigned_tx_bytes
        tx_id: $.results.generate_tx_id.tx_id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```
