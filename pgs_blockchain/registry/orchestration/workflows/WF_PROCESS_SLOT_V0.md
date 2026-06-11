# WF_PROCESS_SLOT_V0

## Header (Mandatory)

- **Artifact Code:** WF_PROCESS_SLOT_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_SLOT_EXECUTION_STARTED_V0, CC_READ_SLOT_CLOCK_V0, CC_PREPARE_SLOT_CONTEXT_V0, CC_INVOKE_BLOCK_PROPOSAL_V0, CC_ADVANCE_SLOT_CLOCK_V0

---

## 1. Intent

Process a single blockchain slot. Reads the current slot clock state, derives the execution context (slot_index, epoch_number, round_number, timestamp), invokes block proposal for this slot, then advances the slot clock. Linear 5-node topology — no loops; the Collatz pattern is applied at the consensus loop level.

---

## 2. Rationale

Each slot execution is atomic: one simulation_id + one slot_number yields one block proposal and one slot clock advance. The slot clock read precedes context derivation — context is derived from the authoritative clock state, not from the raw intent payload. Advancing the clock is the final step to ensure the slot is marked complete only after the block is successfully proposed.

---

## 3. Execution Graph

```
IN_SLOT_EXECUTION_STARTED_V0
    ├─ ACK → CC_READ_SLOT_CLOCK_V0
    │           ├─ SUCCESS → CC_PREPARE_SLOT_CONTEXT_V0
    │           │               ├─ SUCCESS → CC_INVOKE_BLOCK_PROPOSAL_V0
    │           │               │               ├─ SUCCESS → CC_ADVANCE_SLOT_CLOCK_V0
    │           │               │               │               ├─ SUCCESS → EXIT
    │           │               │               │               ├─ VIOLATION → EXIT
    │           │               │               │               ├─ NOT_FOUND → EXIT
    │           │               │               │               └─ BACKEND_ERROR → EXIT
    │           │               │               ├─ VIOLATION → EXIT
    │           │               │               └─ BACKEND_ERROR → EXIT
    │           │               └─ VIOLATION → EXIT
    │           ├─ VIOLATION → EXIT
    │           ├─ NOT_FOUND → EXIT
    │           └─ BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_SLOT_EXECUTION_STARTED_V0 | IN | Entry intent — validates simulation_id, slot_number, triggered_by |
| CC_READ_SLOT_CLOCK_V0 | CC | Read current slot clock record for this simulation |
| CC_PREPARE_SLOT_CONTEXT_V0 | CC | Derive slot execution context via CT_PURE_DERIVE_SLOT_EPOCH_V0 |
| CC_INVOKE_BLOCK_PROPOSAL_V0 | CC | Invoke WF_PROPOSE_BLOCK_V0 with slot context payload |
| CC_ADVANCE_SLOT_CLOCK_V0 | CC | Advance slot clock current_slot by 1 |
| EXIT | EXIT | Terminal node |

---

## Machine

```yaml
wf_code: WF_PROCESS_SLOT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_PROCESS_SLOT_V0
subdomain: orchestration

core:
  summary: Process a single blockchain slot — read clock, derive context, propose block, advance clock
  start_node: IN_SLOT_EXECUTION_STARTED_V0

  nodes:
    IN_SLOT_EXECUTION_STARTED_V0:
      type: IN
      code: IN_SLOT_EXECUTION_STARTED_V0
      next:
        ACK: CC_READ_SLOT_CLOCK_V0
        NACK: EXIT

    CC_READ_SLOT_CLOCK_V0:
      type: CC
      code: CC_READ_SLOT_CLOCK_V0
      inputs:
        simulation_id: $.payload.simulation_id
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_PREPARE_SLOT_CONTEXT_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_PREPARE_SLOT_CONTEXT_V0:
      type: CC
      code: CC_PREPARE_SLOT_CONTEXT_V0
      inputs:
        slot_number: $.payload.slot_number
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_INVOKE_BLOCK_PROPOSAL_V0
        VIOLATION: EXIT

    CC_INVOKE_BLOCK_PROPOSAL_V0:
      type: CC
      code: CC_INVOKE_BLOCK_PROPOSAL_V0
      inputs:
        slot_index: $.results.CC_PREPARE_SLOT_CONTEXT_V0.slot_index
        epoch_number: $.results.CC_PREPARE_SLOT_CONTEXT_V0.epoch_number
        round_number: $.results.CC_PREPARE_SLOT_CONTEXT_V0.round_number
        timestamp: $.results.CC_PREPARE_SLOT_CONTEXT_V0.timestamp
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: CC_ADVANCE_SLOT_CLOCK_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_ADVANCE_SLOT_CLOCK_V0:
      type: CC
      code: CC_ADVANCE_SLOT_CLOCK_V0
      inputs:
        simulation_id: $.payload.simulation_id
        triggered_by: $.payload.triggered_by
      next:
        SUCCESS: EXIT
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED

extensions:
  subdomain: orchestration
  notes:
    - Linear 5-node topology — no loops; Collatz pattern applied at CC_RUN_SLOT_SEQUENCE_V0 level
    - CC_READ_SLOT_CLOCK_V0 reads the slot clock — NOT_FOUND is a hard exit (simulation not initialized)
    - CC_PREPARE_SLOT_CONTEXT_V0 uses {{timestamp}} internally for slot_start_ts — no binding needed
    - CC_ADVANCE_SLOT_CLOCK_V0 reads internally before writing — no current_slot binding needed from WF
    - slot_number comes from intent payload ($.payload.slot_number), not from the slot clock read
    - Block proposal failure (VIOLATION or BACKEND_ERROR) exits before slot clock is advanced
    - authority: AC_SYSTEM_V0
```
