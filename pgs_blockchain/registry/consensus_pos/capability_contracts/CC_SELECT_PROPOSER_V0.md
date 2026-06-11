# CC_SELECT_PROPOSER_V0

## Header (Mandatory)

- **Artifact Code:** CC_SELECT_PROPOSER_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_SELECT_PROPOSER_V0

---

## 1. Intent

Select the block proposer for a given consensus round from the set of eligible validators using deterministic round-robin selection.

---

## 2. Rationale

Proposer selection is a pure deterministic function. Wrapping CT_PURE_SELECT_PROPOSER_V0 in a CC gives it a named outcome surface (SUCCESS / VIOLATION) and positions it as a routable DAG node within WF_PROPOSE_BLOCK_V0.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_SELECT_PROPOSER_V0 | CT | Select proposer by round_number modulo |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| eligible_validators | array | true | Array of active validator records (each must have actor_id) |
| round_number | integer | true | Non-negative consensus round number |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| proposer_id | string | actor_id of the selected proposer |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Proposer selected; proposer_id populated |
| VIOLATION | eligible_validators empty or round_number negative |

---

## 7. Failure Semantics

- VIOLATION propagates from CT_PURE_SELECT_PROPOSER_V0 hard-fail conditions
- No BACKEND_ERROR — pure transform; no storage access

---

## Machine

```yaml
cc_code: CC_SELECT_PROPOSER_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Select block proposer for a consensus round via deterministic round-robin

  inputs:
    eligible_validators:
      type: array
      required: true
      items:
        type: object
    round_number:
      type: integer
      required: true

  outputs:
    proposer_id:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: select_proposer
      transform: blockchain::CT_PURE_SELECT_PROPOSER_V0
      inputs:
        eligible_validators: $.inputs.eligible_validators
        round_number: $.inputs.round_number
      outputs:
        proposer_id: $.capability_result.proposer_id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: consensus_pos
```
