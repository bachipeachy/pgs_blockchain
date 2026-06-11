# WF_RUN_CONSENSUS_SLOTS_V0

## Header (Mandatory)

- **Artifact Code:** WF_RUN_CONSENSUS_SLOTS_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_CONSENSUS_SLOTS_V0, CC_EXECUTE_SLOT_SEQUENCE_V0, CC_VERIFY_SLOT_RESULTS_V0

---

## 1. Intent

Execute a finite ordered sequence of consensus slots and assert post-run invariants. The slot loop is absorbed inside CC_EXECUTE_SLOT_SEQUENCE_V0 (Collatz pattern) — this WF DAG is linear (3 nodes: IN → execute → verify → EXIT).

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration must be absorbed inside a CC (Collatz pattern). CC_EXECUTE_SLOT_SEQUENCE_V0 contains the slot loop and invokes all governed WFs per slot via CS_WORKFLOW_GATEWAY_V0. This WF remains linear: admit the payload, execute the sequence, assert the result.

CC_VERIFY_SLOT_RESULTS_V0 is a post-run assertion that runs after CC_EXECUTE_SLOT_SEQUENCE_V0 returns SUCCESS. It verifies that at least one block was proposed and all eight typed transaction types are represented in the TRANSACTION store. The assertion runs unconditionally on the SUCCESS path — it is not optional.

---

## 3. Execution Graph

```
IN_CONSENSUS_SLOTS_V0
    ├─ ACK → CC_EXECUTE_SLOT_SEQUENCE_V0
    │           ├─ SUCCESS → CC_VERIFY_SLOT_RESULTS_V0
    │           │               ├─ SUCCESS → EXIT
    │           │               ├─ VIOLATION → EXIT
    │           │               └─ BACKEND_ERROR → EXIT
    │           ├─ VIOLATION → EXIT
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_CONSENSUS_SLOTS_V0 | IN | Entry intent — validates slot_schedule is non-empty and triggered_by is present |
| CC_EXECUTE_SLOT_SEQUENCE_V0 | CC | Collatz slot loop — executes all slots via governed WF invocations |
| CC_VERIFY_SLOT_RESULTS_V0 | CC | Post-run assertion — verifies at least one PROPOSED block and all 8 tx_types present |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

slot_schedule must be a non-empty array of slot descriptors. triggered_by must be a non-empty string. Validated by IN_CONSENSUS_SLOTS_V0.

---

## Machine

```yaml
wf_code: WF_RUN_CONSENSUS_SLOTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_RUN_CONSENSUS_SLOTS_V0
subdomain: consensus_pos

core:
  summary: Execute a finite consensus slot sequence and assert post-run invariants
  start_node: IN_CONSENSUS_SLOTS_V0

  nodes:
    IN_CONSENSUS_SLOTS_V0:
      type: IN
      code: IN_CONSENSUS_SLOTS_V0
      next:
        ACK: CC_EXECUTE_SLOT_SEQUENCE_V0
        NACK: EXIT

    CC_EXECUTE_SLOT_SEQUENCE_V0:
      type: CC
      code: CC_EXECUTE_SLOT_SEQUENCE_V0
      inputs:
        slot_schedule: $.payload.slot_schedule
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_VERIFY_SLOT_RESULTS_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_VERIFY_SLOT_RESULTS_V0:
      type: CC
      code: CC_VERIFY_SLOT_RESULTS_V0
      inputs:
        slots_executed: $.results.CC_EXECUTE_SLOT_SEQUENCE_V0.slots_executed
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED

extensions:
  subdomain: consensus_pos
  lifecycle:
    status: RETIRED
    superseded_by: blockchain::WF_RUN_CHAIN_SIMULATION_V0
  notes:
    - Linear WF DAG (3 nodes) — loop absorbed inside CC_EXECUTE_SLOT_SEQUENCE_V0 (Collatz pattern)
    - CC_VERIFY_SLOT_RESULTS_V0 runs unconditionally after SUCCESS — post-run assertion is mandatory
    - VIOLATION from CC_EXECUTE_SLOT_SEQUENCE_V0 means a slot WF returned non-SUCCESS — slot run halted
    - VIOLATION from CC_VERIFY_SLOT_RESULTS_V0 means invariants not met (no PROPOSED block or missing tx_type)
    - All store writes occur through owned CCs invoked via CS_WORKFLOW_GATEWAY_V0 inside CC_EXECUTE_SLOT_SEQUENCE_V0
```
