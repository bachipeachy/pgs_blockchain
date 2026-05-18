# TEST_DATA_CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0

## Machine

```yaml
test_data_code: blockchain::TEST_DATA_CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
  description: |
    Test extraction of transaction fields from wallet record.
  target_artifact: CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
ct_fqdn: "blockchain::CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0"
```

## Purpose

Test extraction of transaction fields from wallet record.

## Test Cases

### Case 1: extract_fields_standard

**Description:** Extract fields from a standard wallet record.

```yaml
case_id: extract_fields_standard
bindings:
  wallet_record:
    actor_id: "ACTOR_01"
    addresses:
      eoa:
        - address: "0x1234567890123456789012345678901234567890"
    state:
      eoa:
        nonce: 5

expected:
  from_address: "0x1234567890123456789012345678901234567890"
  current_nonce: 5
  actor_id: "ACTOR_01"
```
