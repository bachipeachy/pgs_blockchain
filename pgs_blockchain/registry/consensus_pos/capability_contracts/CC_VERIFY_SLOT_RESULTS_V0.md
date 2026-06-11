# CC_VERIFY_SLOT_RESULTS_V0

## Header (Mandatory)

- **Artifact Code:** CC_VERIFY_SLOT_RESULTS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CT_PURE_FILTER_RECORDS_V0

---

## 1. Intent

Post-run assertion CC. Verify that at least one block was proposed (status=PROPOSED in BLOCKS). Assertion is batch-size-agnostic: passes as long as one PROPOSED block exists. Read-only — no writes of any kind.

---

## 2. Rationale

After CC_EXECUTE_SLOT_SEQUENCE_V0 completes, the BLOCKS store must reflect a successful slot run: at least one block proposed. The assertion is intentionally batch-size-agnostic — it does not require a specific number of slots to have produced blocks.

CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when no records match the status=PROPOSED filter, making it the count ≥ 1 assertion for proposed blocks.

CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for an empty store (substrate invariant — empty is not NOT_FOUND). After a slot run, BLOCKS must be non-empty; if the CT filter finds no PROPOSED blocks, the CC exits VIOLATION.

Cross-subdomain read rule: BLOCKS is block-subdomain-owned — accessed read-only.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | LIST BLOCKS store → raw block list |
| 2 | CT_PURE_FILTER_RECORDS_V0 | CT | Filter: status=PROPOSED → proposed_blocks (VIOLATION if none) |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| slots_executed | integer | true | Number of slots executed by CC_EXECUTE_SLOT_SEQUENCE_V0 (bound from WF) |

---

## 5. Outputs

No data outputs. This CC is assertion-only — the result is the outcome code.

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | At least one PROPOSED block found in BLOCKS store |
| VIOLATION | No PROPOSED blocks found |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION from any filter step propagates as CC VIOLATION
- BACKEND_ERROR on store unavailability propagates as hard failure
- Read-only — no partial writes possible

---

## Machine

```yaml
cc_code: CC_VERIFY_SLOT_RESULTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Post-run assertion — verify at least one PROPOSED block in BLOCKS store (batch-size-agnostic)

  inputs:
    slots_executed:
      type: integer
      required: true

  outputs: {}

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: list_blocks
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: BLOCKS
      op: LIST
      inputs: {}
      outputs:
        block_list: $.capability_result.records
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: filter_proposed_blocks
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: filter_proposed_blocks
      transform: capability_transforms::CT_PURE_FILTER_RECORDS_V0
      inputs:
        source: $.results.list_blocks.block_list
        filter:
          status: PROPOSED
      outputs:
        proposed_blocks: $.capability_result.extracted
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: consensus_pos
  notes:
    - Read-only CC — no writes to any store
    - CS_MUTABLE_JSON_V0 LIST returns SUCCESS + [] for empty store (substrate invariant); CT_PURE_FILTER_RECORDS_V0 raises VIOLATION when source is empty or filter matches nothing — used as count ≥ 1 assertion
    - BLOCKS is block-subdomain-owned — accessed read-only
```
