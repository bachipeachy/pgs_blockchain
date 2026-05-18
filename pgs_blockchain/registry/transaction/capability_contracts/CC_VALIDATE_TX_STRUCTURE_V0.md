# CC_VALIDATE_TX_STRUCTURE_V0

## Header (Mandatory)

- **Artifact Code:** CC_VALIDATE_TX_STRUCTURE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_VALIDATE_RECORD_STRUCTURE_V0

---

## 1. Intent

Validate transaction field types, formats, and completeness.

---

## 2. Rationale

Structural validation ensures all transaction fields meet type and format
requirements before any downstream processing. The CC binds domain-specific
validation rules; the infrastructure atom performs generic validation.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_VALIDATE_RECORD_STRUCTURE_V0 | CT | VALIDATE_RECORD_STRUCTURE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| to_address | string | true | Destination address |
| value | string | true | Transfer value in wei |
| gas_limit | integer | false | Gas limit |
| max_fee_per_gas | string | false | Max fee per gas |
| max_priority_fee_per_gas | string | false | Max priority fee |
| data | string | false | Transaction data |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | SUCCESS or VIOLATION |
| violations | array | List of validation violations |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All fields valid |
| VIOLATION | One or more fields invalid (TX_STRUCTURE_INVALID) |

---

## Machine

```yaml
cc_code: CC_VALIDATE_TX_STRUCTURE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Validate transaction field structure

  inputs:
    to_address:
      type: string
      required: true
    value:
      type: string
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

  outputs:
    result_status:
      type: string
    violations:
      type: array

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: validate_tx_structure
      transform: capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
      op: VALIDATE_RECORD_STRUCTURE
      inputs:
        record:
          to_address: $.inputs.to_address
          value: $.inputs.value
          gas_limit: $.inputs.gas_limit
          max_fee_per_gas: $.inputs.max_fee_per_gas
          max_priority_fee_per_gas: $.inputs.max_priority_fee_per_gas
          data: $.inputs.data
        schema:
          to_address:
            type: hex_string
            required: true
            pattern: "^0x[0-9a-fA-F]{40}$"
          value:
            type: integer_string
            required: true
            min_value: 0
          gas_limit:
            type: integer
            min_value: 1
          max_fee_per_gas:
            type: integer_string
            min_value: 0
          max_priority_fee_per_gas:
            type: integer_string
            min_value: 0
            lte_field: max_fee_per_gas
          data:
            type: hex_string
      outputs:
        result_status: $.capability_result.result_status
        violations: $.capability_result.violations
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

  error_codes:
    VIOLATION: TX_STRUCTURE_INVALID
```
