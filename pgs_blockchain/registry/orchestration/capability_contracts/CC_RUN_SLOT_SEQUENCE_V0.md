# CC_RUN_SLOT_SEQUENCE_V0

## Header (Mandatory)

- **Artifact Code:** CC_RUN_SLOT_SEQUENCE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_WORKFLOW_LOOP_V0

---

## 1. Intent

Execute the ordered slot sequence for a simulation run. For each slot number in `slot_schedule`, invoke `WF_PROCESS_SLOT_V0` with `simulation_id` and the item slot number. This CC absorbs the slot loop internally (Collatz pattern) — the governing WF (WF_RUN_CONSENSUS_LOOP_V0) DAG is linear.

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration must be absorbed inside a CC (Collatz pattern). This CC is the loop container for the finite consensus slot run. All domain behavior (slot clock read/advance, block proposal) executes inside `WF_PROCESS_SLOT_V0`. This CC contains no domain logic — it declares a fully parametric dispatch to CS_WORKFLOW_LOOP_V0, which iterates the slot_schedule array and invokes WF_PROCESS_SLOT_V0 per item.

Termination: the slot loop exits when `slot_schedule` is exhausted. Finite termination is guaranteed by the non-empty finite array declared in IN_CONSENSUS_LOOP_STARTED_V0.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_WORKFLOW_LOOP_V0 | CS | EXECUTE_SEQUENCE — iterate slot_schedule; dispatch WF_PROCESS_SLOT_V0 per slot number |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; injected into every WF_PROCESS_SLOT_V0 invocation |
| `slot_schedule` | array | true | Non-empty ordered list of slot descriptor objects `{slot_number: integer}` to execute |
| `triggered_by` | string | true | Actor ID or system trigger reference; injected into every WF_PROCESS_SLOT_V0 invocation |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `slots_executed` | integer | Number of slot numbers processed (`items_processed` from CS) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All slot numbers processed; all WF_PROCESS_SLOT_V0 invocations returned SUCCESS |
| VIOLATION | Any WF_PROCESS_SLOT_V0 invocation returned non-SUCCESS; loop halted |
| BACKEND_ERROR | Loop executor or storage unavailable |

---

## 7. Failure Semantics

- VIOLATION from any WF_PROCESS_SLOT_V0 invocation propagates as CC VIOLATION — the slot run halts; remaining slots do not execute
- BACKEND_ERROR propagates as a hard failure
- No partial commit — VIOLATION exits before remaining slots execute

---

## Machine

```yaml
cc_code: CC_RUN_SLOT_SEQUENCE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Collatz-pattern slot loop — execute all slots in slot_schedule via CS_WORKFLOW_LOOP_V0

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; injected into every WF_PROCESS_SLOT_V0 payload
    slot_schedule:
      type: array
      required: true
      description: "Non-empty ordered list of slot descriptor objects {slot_number: integer} to execute"
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string
    slots_executed:
      type: integer

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: execute_slot_sequence
      side_effect: capability_side_effects::CS_WORKFLOW_LOOP_V0
      op: EXECUTE_SEQUENCE
      inputs:
        sequence: $.inputs.slot_schedule
        triggered_by: $.inputs.triggered_by
        item_wf:
          code: blockchain::WF_PROCESS_SLOT_V0
          payload_fields:
            slot_number: slot_number
          inject:
            simulation_id: $.inputs.simulation_id
            triggered_by: $.inputs.triggered_by
      outputs:
        slots_executed: $.capability_result.items_processed
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - Collatz pattern — loop absorbed inside this CC; WF_RUN_CONSENSUS_LOOP_V0 DAG is linear
    - CS_WORKFLOW_LOOP_V0 EXECUTE_SEQUENCE is the governed side effect — zero domain knowledge in substrate
    - slot_schedule items are slot descriptor dicts {slot_number: integer}; payload_fields maps dest slot_number → source slot_number in item
    - simulation_id injected into every WF_PROCESS_SLOT_V0 invocation
    - VIOLATION from any WF_PROCESS_SLOT_V0 invocation halts the loop — no partial execution
    - Termination guaranteed by finite slot_schedule declared in IN_CONSENSUS_LOOP_STARTED_V0
```
