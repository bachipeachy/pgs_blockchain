# CC_QUERY_ELIGIBLE_VALIDATORS_V0

## Header (Mandatory)

- **Artifact Code:** CC_QUERY_ELIGIBLE_VALIDATORS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_FILTER_RECORDS_V0

---

## 1. Intent

Query the VALIDATOR store for all registered validators, then filter to those eligible for consensus participation (status=ACTIVE_ONGOING and effective_balance present).

---

## 2. Rationale

Proposer selection requires a clean list of eligible validators. Eligibility filtering is a pure transform step (CT_PURE_FILTER_RECORDS_V0) applied after the raw store list is retrieved. This CC is the sole entry point for eligible validator resolution — no other CC or WF may filter validators independently.

VIOLATION is the exit when no eligible validators exist (empty VALIDATOR store or none with ACTIVE_ONGOING status and stake) — CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when no records match the filter. WF_PROPOSE_BLOCK_V0 routes this VIOLATION to EXIT without recording a round (valid bootstrap behavior).

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | LIST VALIDATOR store → raw validator list |
| 2 | CT_PURE_FILTER_RECORDS_V0 | CT | Filter: status=ACTIVE_ONGOING AND effective_balance present |

---

## 4. Inputs

No inputs required. This CC reads directly from the VALIDATOR store.

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| eligible_validators | array | Filtered list of active validator records with stake |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | One or more eligible validators found; eligible_validators populated |
| VIOLATION | No eligible validators found (empty pool or none with ACTIVE_ONGOING status and stake), or storage data malformed |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION covers both "no eligible validators" (CT filter found no matches) and "malformed store data"
- WF_PROPOSE_BLOCK_V0 routes VIOLATION → EXIT without recording a round (valid during bootstrap)
- BACKEND_ERROR propagates as a hard failure

---

## Machine

```yaml
cc_code: CC_QUERY_ELIGIBLE_VALIDATORS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Query VALIDATOR store and filter to eligible consensus participants

  inputs: {}

  outputs:
    eligible_validators:
      type: array
      items:
        type: object

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: list_validators
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: VALIDATOR
      op: LIST
      inputs: {}
      outputs:
        validator_list: $.capability_result.records
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: filter_eligible
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: filter_eligible
      transform: capability_transforms::CT_PURE_FILTER_RECORDS_V0
      inputs:
        source: $.results.list_validators.validator_list
        filter:
          status: ACTIVE_ONGOING
          effective_balance: present
      outputs:
        eligible_validators: $.capability_result.extracted
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: consensus_pos
  notes:
    - CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for empty store (substrate invariant — empty is not NOT_FOUND)
    - CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when no records match — covers both empty store and no ACTIVE_ONGOING validators
    - VIOLATION from this CC causes WF_PROPOSE_BLOCK_V0 to EXIT without recording a round (valid during bootstrap)
    - Eligibility filter: status=ACTIVE_ONGOING AND effective_balance present
    - Functional runtime dependency on WF_REGISTER_VALIDATOR_V0 being operational (validators must be registered before eligibility queries return results)
```
