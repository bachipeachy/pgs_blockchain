# CC_RECORD_SIMULATION_SUMMARY_V0

## Header (Mandatory)

- **Artifact Code:** CC_RECORD_SIMULATION_SUMMARY_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Append a simulation summary record to the SIMULATION_SUMMARY store. Records the final outcome and per-worker results from a completed chain simulation run.

---

## 2. Rationale

The simulation summary is an append-only audit record. It captures `simulation_outcome` (passed by the calling WF based on dispatch routing) and `results` (the per-worker result array from CC_DISPATCH_SIMULATION_WORKERS_V0). This CC is invoked for both SUCCESS and PARTIAL_FAILURE dispatch outcomes — the summary is always recorded regardless of whether all workers succeeded.

`simulation_id` is the stream key — all summary records for a simulation run are correlated by it.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; used as stream key |
| `simulation_outcome` | string | true | Final simulation outcome — SUCCESS or PARTIAL_FAILURE; passed by WF routing from CC_DISPATCH_SIMULATION_WORKERS_V0 result_status |
| `results` | array | true | Per-worker result array from CC_DISPATCH_SIMULATION_WORKERS_V0; each entry: `{code, result_status, outputs}` |
| `triggered_by` | string | true | Actor ID or system trigger reference |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Summary record appended successfully |
| VIOLATION | Invalid input (empty simulation_id, malformed results) |
| BACKEND_ERROR | Storage write failure |

---

## 7. Failure Semantics

- VIOLATION on empty `simulation_id` or malformed `results` array
- BACKEND_ERROR if the SIMULATION_SUMMARY store is unavailable
- No ALREADY_EXISTS — CS_APPENDONLY_JSONL_V0 APPEND is unconditional

---

## Machine

```yaml
cc_code: CC_RECORD_SIMULATION_SUMMARY_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Append simulation summary record to SIMULATION_SUMMARY store

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; stream key for the summary record
    simulation_outcome:
      type: string
      required: true
      description: Final outcome — SUCCESS or PARTIAL_FAILURE; sourced from CC_DISPATCH_SIMULATION_WORKERS_V0 result_status
    results:
      type: array
      required: true
      description: Per-worker result array; each entry carries code, result_status, outputs
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: append_simulation_summary
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: SIMULATION_SUMMARY
      op: APPEND
      inputs:
        stream_id: $.inputs.simulation_id
        actor_id: $.inputs.triggered_by
        record:
          simulation_id: $.inputs.simulation_id
          simulation_outcome: $.inputs.simulation_outcome
          worker_results: $.inputs.results
          completed_at: "{{timestamp}}"
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - SIMULATION_SUMMARY store is defined in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
    - Always invoked — summary recorded for both SUCCESS and PARTIAL_FAILURE dispatch outcomes
    - simulation_outcome is passed by WF routing, not computed inside this CC
    - results array correlated by code (workflow FQDN) per CS_CONCURRENT_WORKFLOWS_V0 contract
```
