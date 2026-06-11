# WF_RUN_CONSENSUS_LOOP_V0

## Header (Mandatory)

- **Artifact Code:** WF_RUN_CONSENSUS_LOOP_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_CONSENSUS_LOOP_STARTED_V0, CC_RUN_SLOT_SEQUENCE_V0

---

## 1. Intent

Execute the ordered slot sequence for a simulation run. Absorbs the slot loop inside CC_RUN_SLOT_SEQUENCE_V0 (Collatz pattern) — this WF DAG is linear (2 nodes: IN → execute → EXIT).

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration is absorbed inside a CC (Collatz pattern). CC_RUN_SLOT_SEQUENCE_V0 contains the slot loop and invokes WF_PROCESS_SLOT_V0 per slot number via CS_WORKFLOW_LOOP_V0. This WF remains linear: admit the payload, execute the slot sequence, exit.

---

## 3. Execution Graph

```
IN_CONSENSUS_LOOP_STARTED_V0
    ├─ ACK → CC_RUN_SLOT_SEQUENCE_V0
    │           ├─ SUCCESS → EXIT
    │           ├─ VIOLATION → EXIT
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_CONSENSUS_LOOP_STARTED_V0 | IN | Entry intent — validates simulation_id, slot_schedule, triggered_by |
| CC_RUN_SLOT_SEQUENCE_V0 | CC | Collatz slot loop — iterates slot_schedule; invokes WF_PROCESS_SLOT_V0 per slot |
| EXIT | EXIT | Terminal node |

---

## Machine

```yaml
wf_code: WF_RUN_CONSENSUS_LOOP_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_RUN_CONSENSUS_LOOP_V0
subdomain: orchestration

core:
  summary: Execute ordered slot sequence via Collatz-pattern CC_RUN_SLOT_SEQUENCE_V0
  start_node: IN_CONSENSUS_LOOP_STARTED_V0

  nodes:
    IN_CONSENSUS_LOOP_STARTED_V0:
      type: IN
      code: IN_CONSENSUS_LOOP_STARTED_V0
      next:
        ACK: CC_RUN_SLOT_SEQUENCE_V0
        NACK: EXIT

    CC_RUN_SLOT_SEQUENCE_V0:
      type: CC
      code: CC_RUN_SLOT_SEQUENCE_V0
      inputs:
        simulation_id: $.payload.simulation_id
        slot_schedule: $.payload.slot_schedule
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
    - Linear 2-node topology — Collatz pattern absorbed in CC_RUN_SLOT_SEQUENCE_V0
    - slot_schedule is a pre-expanded array of integer slot numbers from IN_CONSENSUS_LOOP_STARTED_V0
    - VIOLATION from CC means at least one WF_PROCESS_SLOT_V0 invocation failed — loop halted
    - authority: AC_SYSTEM_V0
```
