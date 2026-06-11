# CC_INVOKE_BLOCK_PROPOSAL_V0

## Header (Mandatory)

- **Artifact Code:** CC_INVOKE_BLOCK_PROPOSAL_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_WORKFLOW_GATEWAY_V0

---

## 1. Intent

Invoke `WF_PROPOSE_BLOCK_V0` via the workflow gateway for the current slot execution context. Maps slot context fields into the block proposal payload: `slot_index` → `slot`, `epoch_number` → `epoch`.

---

## 2. Rationale

Block proposal is the terminal action for each slot in the consensus loop. This CC bridges the orchestration subdomain to the block subdomain by invoking `WF_PROPOSE_BLOCK_V0` as a governed sub-workflow. Field mapping (`slot_index` → `slot`, `epoch_number` → `epoch`) is declared explicitly here — this is the single point of truth for the payload contract translation.

NOT_FOUND from the gateway means the target workflow is not registered in the snapshot — this is a hard BACKEND_ERROR, not a recoverable condition.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_WORKFLOW_GATEWAY_V0 | CS | EXECUTE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slot_index` | integer | true | Intra-epoch slot position; maps to `slot` in WF_PROPOSE_BLOCK_V0 payload |
| `epoch_number` | integer | true | Monotonically increasing epoch counter; maps to `epoch` in WF_PROPOSE_BLOCK_V0 payload |
| `round_number` | integer | true | Pass-through of global slot counter; maps to `round_number` in WF_PROPOSE_BLOCK_V0 payload |
| `timestamp` | string | true | Slot start timestamp; maps to `timestamp` in WF_PROPOSE_BLOCK_V0 payload |
| `triggered_by` | string | true | Actor ID or system trigger reference; injected into WF_PROPOSE_BLOCK_V0 payload |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `execution_result` | object | Full result from WF_PROPOSE_BLOCK_V0 execution |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | WF_PROPOSE_BLOCK_V0 executed and returned SUCCESS |
| VIOLATION | WF_PROPOSE_BLOCK_V0 returned VIOLATION or NACK |
| NOT_FOUND | WF_PROPOSE_BLOCK_V0 not registered in snapshot — surfaced as BACKEND_ERROR |
| BACKEND_ERROR | Gateway or execution infrastructure unavailable |

---

## 7. Failure Semantics

- SUCCESS from gateway → propagate as SUCCESS
- NOT_FOUND from gateway → exits as BACKEND_ERROR — missing WF is a configuration failure, not a domain error
- BACKEND_ERROR from gateway → exits as BACKEND_ERROR
- Non-SUCCESS from WF_PROPOSE_BLOCK_V0 execution_result → exits as VIOLATION

---

## Machine

```yaml
cc_code: CC_INVOKE_BLOCK_PROPOSAL_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Invoke WF_PROPOSE_BLOCK_V0 via workflow gateway with slot context payload

  inputs:
    slot_index:
      type: integer
      required: true
      description: Intra-epoch slot position; maps to 'slot' in block proposal payload
    epoch_number:
      type: integer
      required: true
      description: Epoch counter; maps to 'epoch' in block proposal payload
    round_number:
      type: integer
      required: true
      description: Global slot counter pass-through; maps to 'round_number' in block proposal payload
    timestamp:
      type: string
      required: true
      description: Slot start timestamp; maps to 'timestamp' in block proposal payload
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference; injected into WF_PROPOSE_BLOCK_V0 payload

  outputs:
    result_status:
      type: string
    execution_result:
      type: object
      description: Full result from WF_PROPOSE_BLOCK_V0

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: invoke_block_proposal
      side_effect: capability_side_effects::CS_WORKFLOW_GATEWAY_V0
      op: EXECUTE
      inputs:
        workflow_code: blockchain::WF_PROPOSE_BLOCK_V0
        payload:
          slot: $.inputs.slot_index
          epoch: $.inputs.epoch_number
          round_number: $.inputs.round_number
          timestamp: $.inputs.timestamp
          triggered_by: $.inputs.triggered_by
      outputs:
        result_status: $.capability_result.result_status
        execution_result: $.capability_result.execution_result
      result_surface: [SUCCESS, NOT_FOUND, BACKEND_ERROR]
      on_result:
        SUCCESS: evaluate_execution_result
        NOT_FOUND: remap_to_backend_error
        BACKEND_ERROR: exit

  evaluation:
    evaluate_execution_result:
      condition: $.execution_result.status == "SUCCESS"
      on_true: SUCCESS
      on_false: VIOLATION
    remap_to_backend_error:
      condition: $.capability_result.result_status == "NOT_FOUND"
      on_true: BACKEND_ERROR
      on_false: BACKEND_ERROR

extensions:
  subdomain: orchestration
  notes:
    - Field mapping — slot_index → slot, epoch_number → epoch; declared explicitly here
    - NOT_FOUND routes to exit as BACKEND_ERROR — missing WF is a snapshot configuration failure
    - execution_result carries the full WF_PROPOSE_BLOCK_V0 output for downstream inspection
    - WF_PROPOSE_BLOCK_V0 payload contract governed by IN_BLOCK_PROPOSED_V0
```
