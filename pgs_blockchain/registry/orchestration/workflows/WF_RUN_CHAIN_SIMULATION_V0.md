# WF_RUN_CHAIN_SIMULATION_V0

## Header (Mandatory)

- **Artifact Code:** WF_RUN_CHAIN_SIMULATION_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** WF_RUN_CONSENSUS_SLOTS_V0
- **Dependencies:** IN_RUN_CHAIN_SIMULATION_V0, CC_INITIALIZE_SLOT_CLOCK_V0, CC_DISPATCH_SIMULATION_WORKERS_V0, CC_RECORD_SIMULATION_SUMMARY_V0

---

## 1. Intent

Run a complete governed chain simulation. Initializes the slot clock, concurrently dispatches the consensus loop and TX workload workers, and records the simulation summary. PARTIAL_FAILURE from dispatch is a recoverable outcome — summary is always recorded.

---

## 2. Rationale

`simulation_id` is the primary isolation boundary established at initialization. All slot clock records and simulation summary records are keyed by it. Concurrent dispatch (CS_CONCURRENT_WORKFLOWS_V0) runs the consensus loop and TX workload as independent workers — neither halts the other on failure. The summary records both SUCCESS and PARTIAL_FAILURE outcomes; only BACKEND_ERROR exits without recording.

---

## 3. Execution Graph

```
IN_RUN_CHAIN_SIMULATION_V0
    ├─ ACK → CC_INITIALIZE_SLOT_CLOCK_V0
    │           ├─ SUCCESS → CC_DISPATCH_SIMULATION_WORKERS_V0
    │           │               ├─ SUCCESS → CC_RECORD_SIMULATION_SUMMARY_V0
    │           │               │               ├─ SUCCESS → EXIT
    │           │               │               ├─ VIOLATION → EXIT
    │           │               │               └─ BACKEND_ERROR → EXIT
    │           │               ├─ PARTIAL_FAILURE → CC_RECORD_SIMULATION_SUMMARY_V0
    │           │               └─ BACKEND_ERROR → EXIT
    │           ├─ VIOLATION → EXIT
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_RUN_CHAIN_SIMULATION_V0 | IN | Entry intent — validates simulation parameters |
| CC_INITIALIZE_SLOT_CLOCK_V0 | CC | Initialize slot clock record keyed by simulation_id |
| CC_DISPATCH_SIMULATION_WORKERS_V0 | CC | Concurrently run consensus loop + TX workload workers |
| CC_RECORD_SIMULATION_SUMMARY_V0 | CC | Append simulation summary to SIMULATION_SUMMARY store |
| EXIT | EXIT | Terminal node |

---

## Machine

```yaml
wf_code: WF_RUN_CHAIN_SIMULATION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_RUN_CHAIN_SIMULATION_V0
subdomain: orchestration

core:
  summary: Run complete chain simulation — init clock, dispatch workers, record summary
  start_node: IN_RUN_CHAIN_SIMULATION_V0

  nodes:
    IN_RUN_CHAIN_SIMULATION_V0:
      type: IN
      code: IN_RUN_CHAIN_SIMULATION_V0
      next:
        ACK: CC_INITIALIZE_SLOT_CLOCK_V0
        NACK: EXIT

    CC_INITIALIZE_SLOT_CLOCK_V0:
      type: CC
      code: CC_INITIALIZE_SLOT_CLOCK_V0
      inputs:
        simulation_id: $.payload.simulation_id
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_DISPATCH_SIMULATION_WORKERS_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_DISPATCH_SIMULATION_WORKERS_V0:
      type: CC
      code: CC_DISPATCH_SIMULATION_WORKERS_V0
      inputs:
        simulation_id: $.payload.simulation_id
        slot_schedule: $.payload.slot_schedule
        tx_interval_seconds: $.payload.tx_interval_seconds
        tx_sequence: $.payload.tx_sequence
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_RECORD_SIMULATION_SUMMARY_V0
        PARTIAL_FAILURE: CC_RECORD_SIMULATION_SUMMARY_V0
        BACKEND_ERROR: EXIT

    CC_RECORD_SIMULATION_SUMMARY_V0:
      type: CC
      code: CC_RECORD_SIMULATION_SUMMARY_V0
      inputs:
        simulation_id: $.payload.simulation_id
        simulation_outcome: $.results.CC_DISPATCH_SIMULATION_WORKERS_V0.result_status
        results: $.results.CC_DISPATCH_SIMULATION_WORKERS_V0.results
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED

extensions:
  subdomain: orchestration
  notes:
    - 4-node topology — init clock → dispatch workers → record summary → exit
    - slot_schedule is a pre-expanded array of integer slot numbers; sourced from payload (seed config or caller)
    - PARTIAL_FAILURE from CC_DISPATCH routes to CC_RECORD — summary always recorded for partial failures
    - BACKEND_ERROR from CC_DISPATCH exits without recording — infrastructure failure
    - simulation_outcome in CC_RECORD is sourced from CC_DISPATCH result_status (SUCCESS or PARTIAL_FAILURE)
    - simulation_id isolation invariant: all slot clock + summary records keyed by simulation_id
    - Supersedes WF_RUN_CONSENSUS_SLOTS_V0 — that WF is RETIRED; this is the orchestration entry point
    - authority: AC_SYSTEM_V0
```
