# WF_RUN_TX_WORKLOAD_V0

## Header (Mandatory)

- **Artifact Code:** WF_RUN_TX_WORKLOAD_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_TX_WORKLOAD_STARTED_V0, CC_RUN_TX_SEQUENCE_V0

---

## 1. Intent

Execute the ordered TX workload sequence. Absorbs the TX loop inside CC_RUN_TX_SEQUENCE_V0 (Collatz pattern) — this WF DAG is linear (2 nodes: IN → execute → EXIT).

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration is absorbed inside a CC (Collatz pattern). CC_RUN_TX_SEQUENCE_V0 contains the TX loop and dispatches each TX spec to the appropriate typed TX workflow by `tx_type`. This WF remains linear: admit the payload, execute the TX sequence, exit.

---

## 3. Execution Graph

```
IN_TX_WORKLOAD_STARTED_V0
    ├─ ACK → CC_RUN_TX_SEQUENCE_V0
    │           ├─ SUCCESS → EXIT
    │           ├─ VIOLATION → EXIT
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_TX_WORKLOAD_STARTED_V0 | IN | Entry intent — validates tx_interval_seconds, tx_sequence, triggered_by |
| CC_RUN_TX_SEQUENCE_V0 | CC | Collatz TX loop — iterates tx_sequence; dispatches by tx_type to typed TX WFs |
| EXIT | EXIT | Terminal node |

---

## Machine

```yaml
wf_code: WF_RUN_TX_WORKLOAD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_RUN_TX_WORKLOAD_V0
subdomain: orchestration

core:
  summary: Execute ordered TX workload sequence via Collatz-pattern CC_RUN_TX_SEQUENCE_V0
  start_node: IN_TX_WORKLOAD_STARTED_V0

  nodes:
    IN_TX_WORKLOAD_STARTED_V0:
      type: IN
      code: IN_TX_WORKLOAD_STARTED_V0
      next:
        ACK: CC_RUN_TX_SEQUENCE_V0
        NACK: EXIT

    CC_RUN_TX_SEQUENCE_V0:
      type: CC
      code: CC_RUN_TX_SEQUENCE_V0
      inputs:
        tx_sequence: $.payload.tx_sequence
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
    - Linear 2-node topology — Collatz pattern absorbed in CC_RUN_TX_SEQUENCE_V0
    - tx_sequence carries fully resolved TX spec objects; no payload construction inside this WF
    - tx_interval_seconds is declared in IN but not passed to CC — CS_WORKFLOW_LOOP_V0 executes sequentially without delay (timing is a runtime infrastructure concern)
    - VIOLATION from CC means at least one typed TX WF invocation failed — loop halted
    - authority: AC_SYSTEM_V0
```
