# TEST_DATA_CT_PURE_BUILD_ETH_TRANSACTION_V0

## Machine

```yaml
test_data_code: blockchain::TEST_DATA_CT_PURE_BUILD_ETH_TRANSACTION_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_BUILD_ETH_TRANSACTION_V0
  description: |
    Test EIP-1559 Ethereum transaction building.
  target_artifact: CT_PURE_BUILD_ETH_TRANSACTION_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_BUILD_ETH_TRANSACTION_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_BUILD_ETH_TRANSACTION_V0
ct_fqdn: "blockchain::CT_PURE_BUILD_ETH_TRANSACTION_V0"
```

## Purpose

Test EIP-1559 Ethereum transaction building.

## Test Cases

### Case 1: basic_valid_tx

**Description:** Build a simple EIP-1559 transfer transaction.

```yaml
case_id: basic_valid_tx
expected_outcome: SUCCESS
bindings:
  chain_id: 1
  nonce: 10
  max_priority_fee_per_gas: "1000000000"
  max_fee_per_gas: "20000000000"
  gas_limit: 21000
  to: "0x1234567890123456789012345678901234567890"
  value: "1000000000000000000"
  data: "0x"
  access_list: []

expected:
  unsigned_tx_bytes: "0x02f0010a843b9aca008504a817c800825208941234567890123456789012345678901234567890880de0b6b3a764000080c0"
```
