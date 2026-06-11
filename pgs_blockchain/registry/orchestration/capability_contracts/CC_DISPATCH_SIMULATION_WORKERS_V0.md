# CC_DISPATCH_SIMULATION_WORKERS_V0

## Header (Mandatory)

- **Artifact Code:** CC_DISPATCH_SIMULATION_WORKERS_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_CONCURRENT_WORKFLOWS_V0

---

## 1. Intent

Concurrently dispatch the two simulation sub-workflows — `WF_RUN_CONSENSUS_LOOP_V0` and `WF_RUN_TX_WORKLOAD_V0` — and collect their results. Both workers run to completion regardless of individual outcomes. Results are correlated by workflow FQDN code.

---

## 2. Rationale

Chain simulation runs two independent workers: the consensus loop (slot sequencing + block proposals) and the TX workload (typed transaction submissions). Concurrent execution maximizes simulation fidelity. No ordering dependency exists between the two workers.

`PARTIAL_FAILURE` is an expected simulation outcome — if one worker fails, the other's results are still meaningful and must be captured. Both SUCCESS and PARTIAL_FAILURE route to `CC_RECORD_SIMULATION_SUMMARY_V0`; only BACKEND_ERROR exits without recording.

Results are correlated by `code` (workflow FQDN) per CS_CONCURRENT_WORKFLOWS_V0 contract — not by array position.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_CONCURRENT_WORKFLOWS_V0 | CS | EXECUTE_CONCURRENT |

**Workers dispatched:**
- `blockchain::WF_RUN_CONSENSUS_LOOP_V0` — consensus slot loop worker
- `blockchain::WF_RUN_TX_WORKLOAD_V0` — TX workload worker

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; injected into WF_RUN_CONSENSUS_LOOP_V0 payload |
| `slot_schedule` | array | true | Pre-expanded ordered list of integer slot numbers; passed to WF_RUN_CONSENSUS_LOOP_V0 |
| `tx_interval_seconds` | integer | true | Interval between TX submissions in seconds; passed to WF_RUN_TX_WORKLOAD_V0 |
| `tx_sequence` | array | true | Non-empty ordered list of TX specs; passed to WF_RUN_TX_WORKLOAD_V0 |
| `triggered_by` | string | true | Actor ID or system trigger reference; injected into both worker payloads |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Aggregate result — SUCCESS, PARTIAL_FAILURE, or BACKEND_ERROR |
| `results` | array | Per-worker result array; each entry: `{code, result_status, outputs}`; correlated by FQDN code |
| `all_succeeded` | boolean | `true` iff both workers returned SUCCESS |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Both workers returned SUCCESS |
| PARTIAL_FAILURE | At least one worker returned non-SUCCESS; other worker still executed |
| BACKEND_ERROR | Execution infrastructure unavailable; no workers were able to run |

---

## 7. Failure Semantics

- PARTIAL_FAILURE is not a fatal error — it routes to CC_RECORD_SIMULATION_SUMMARY_V0 for recording
- BACKEND_ERROR exits without recording — infrastructure failure, not a domain outcome
- All workers execute regardless of peer outcomes — no short-circuit on PARTIAL_FAILURE
- Duplicate workflow codes within a single invocation are a VIOLATION (governance invariant, not expected in this CC)

---

## Machine

```yaml
cc_code: CC_DISPATCH_SIMULATION_WORKERS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Concurrently dispatch consensus loop + TX workload workers; collect results

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; injected into WF_RUN_CONSENSUS_LOOP_V0 payload
    slot_schedule:
      type: array
      required: true
      description: Pre-expanded ordered list of integer slot numbers; passed to WF_RUN_CONSENSUS_LOOP_V0
    tx_interval_seconds:
      type: integer
      required: true
      description: TX submission interval in seconds; passed to WF_RUN_TX_WORKLOAD_V0
    tx_sequence:
      type: array
      required: true
      description: Non-empty ordered list of TX specs; passed to WF_RUN_TX_WORKLOAD_V0
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference; injected into both worker payloads

  outputs:
    result_status:
      type: string
    results:
      type: array
      description: Per-worker results correlated by workflow FQDN code
    all_succeeded:
      type: boolean

  result_status_contract:
    allowed: [SUCCESS, PARTIAL_FAILURE, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: dispatch_concurrent_workers
      side_effect: capability_side_effects::CS_CONCURRENT_WORKFLOWS_V0
      op: EXECUTE_CONCURRENT
      inputs:
        workflows:
          - code: blockchain::WF_RUN_CONSENSUS_LOOP_V0
            payload:
              simulation_id: $.inputs.simulation_id
              slot_schedule: $.inputs.slot_schedule
              triggered_by: $.inputs.triggered_by
          - code: blockchain::WF_RUN_TX_WORKLOAD_V0
            payload:
              tx_interval_seconds: $.inputs.tx_interval_seconds
              tx_sequence: $.inputs.tx_sequence
              triggered_by: $.inputs.triggered_by
        triggered_by: $.inputs.triggered_by
      outputs:
        result_status: $.capability_result.result_status
        results: $.capability_result.results
        all_succeeded: $.capability_result.all_succeeded
      result_surface: [SUCCESS, PARTIAL_FAILURE, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        PARTIAL_FAILURE: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - CS_CONCURRENT_WORKFLOWS_V0 contract — all workers execute; no short-circuit on peer VIOLATION
    - Results correlated by code (FQDN), NOT by array position
    - Both SUCCESS and PARTIAL_FAILURE route to CC_RECORD_SIMULATION_SUMMARY_V0 — summary always recorded
    - BACKEND_ERROR exits without recording — infrastructure failure
    - WF payloads constructed inline — simulation_id and triggered_by injected into consensus loop; tx_interval_seconds and tx_sequence into TX workload
```
