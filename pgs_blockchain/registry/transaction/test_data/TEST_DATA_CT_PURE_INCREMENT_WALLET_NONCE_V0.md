# TEST_DATA_CT_PURE_INCREMENT_WALLET_NONCE_V0

## Machine

```yaml
test_data_code: blockchain::TEST_DATA_CT_PURE_INCREMENT_WALLET_NONCE_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_INCREMENT_WALLET_NONCE_V0
  description: |
    Test wallet nonce increment and reservation.
  target_artifact: CT_PURE_INCREMENT_WALLET_NONCE_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_INCREMENT_WALLET_NONCE_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_INCREMENT_WALLET_NONCE_V0
ct_fqdn: "blockchain::CT_PURE_INCREMENT_WALLET_NONCE_V0"
```

## Purpose

Test wallet nonce increment and reservation.

## Test Cases

### Case 1: increment_from_zero

**Description:** Increment nonce starting from zero.

```yaml
case_id: increment_from_zero
bindings:
  wallet_record:
    actor_id: "ACTOR_01"
    addresses:
      eoa:
        - address: "0x1234567890123456789012345678901234567890"
    state:
      eoa:
        nonce: 0

expected:
  updated_wallet_record:
    actor_id: "ACTOR_01"
    addresses:
      eoa:
        - address: "0x1234567890123456789012345678901234567890"
    state:
      eoa:
        nonce: 1
  nonce: 0
```

### Case 2: increment_from_positive

**Description:** Increment nonce starting from a positive value.

```yaml
case_id: increment_from_positive
bindings:
  wallet_record:
    actor_id: "ACTOR_02"
    addresses:
      eoa:
        - address: "0xdeadbeef00000000000000000000000000000001"
    state:
      eoa:
        nonce: 42

expected:
  updated_wallet_record:
    actor_id: "ACTOR_02"
    addresses:
      eoa:
        - address: "0xdeadbeef00000000000000000000000000000001"
    state:
      eoa:
        nonce: 43
  nonce: 42
```
