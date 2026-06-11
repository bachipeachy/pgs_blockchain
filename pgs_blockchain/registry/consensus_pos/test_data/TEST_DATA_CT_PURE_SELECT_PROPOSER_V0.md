# TEST_DATA_CT_PURE_SELECT_PROPOSER_V0

## Machine

```yaml
test_data_code: blockchain::TEST_DATA_CT_PURE_SELECT_PROPOSER_V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0
version: 0

core:
  summary: Test data for CT_PURE_SELECT_PROPOSER_V0
  description: |
    Test deterministic proposer selection by round_number modulo eligible_validators length.
  target_artifact: CT_PURE_SELECT_PROPOSER_V0
```

## Artifact

```yaml
artifact_type: TEST_DATA
fqdn_id: "test_data.ct::TEST_DATA_CT_PURE_SELECT_PROPOSER_V0"
version: V0
status: canonical
```

## Target

```yaml
ct_code: CT_PURE_SELECT_PROPOSER_V0
ct_fqdn: "blockchain::CT_PURE_SELECT_PROPOSER_V0"
```

## Purpose

Verify deterministic round-robin proposer selection and hard-failure on invalid inputs.

## Test Cases

### Case 1: select_first_proposer

**Description:** Round 0 selects index 0 (first validator).

```yaml
case_id: select_first_proposer
expected_outcome: SUCCESS
bindings:
  eligible_validators:
    - actor_id: "ACTOR_01"
      stake: "1000"
      enrollment_status: "ACTIVE"
    - actor_id: "ACTOR_02"
      stake: "2000"
      enrollment_status: "ACTIVE"
    - actor_id: "ACTOR_03"
      stake: "1500"
      enrollment_status: "ACTIVE"
  round_number: 0

expected:
  proposer_id: "ACTOR_01"
```

### Case 2: select_by_modulo

**Description:** Round number wraps around using modulo — round 4 with 3 validators selects index 1.

```yaml
case_id: select_by_modulo
expected_outcome: SUCCESS
bindings:
  eligible_validators:
    - actor_id: "ACTOR_01"
      stake: "1000"
      enrollment_status: "ACTIVE"
    - actor_id: "ACTOR_02"
      stake: "2000"
      enrollment_status: "ACTIVE"
    - actor_id: "ACTOR_03"
      stake: "1500"
      enrollment_status: "ACTIVE"
  round_number: 4

expected:
  proposer_id: "ACTOR_02"
```

### Case 3: single_validator

**Description:** Single eligible validator is always selected regardless of round number.

```yaml
case_id: single_validator
expected_outcome: SUCCESS
bindings:
  eligible_validators:
    - actor_id: "ACTOR_01"
      stake: "1000"
      enrollment_status: "ACTIVE"
  round_number: 99

expected:
  proposer_id: "ACTOR_01"
```
