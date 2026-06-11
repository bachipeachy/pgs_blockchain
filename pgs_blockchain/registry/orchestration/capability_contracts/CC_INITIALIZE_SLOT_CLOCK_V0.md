# CC_INITIALIZE_SLOT_CLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CC_INITIALIZE_SLOT_CLOCK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Initialize the slot clock for a simulation run. Writes the initial slot clock record keyed by `simulation_id` to the SLOT_CLOCK store.

---

## 2. Rationale

The slot clock is the central state object for slot sequencing in a simulation run. All CCs that read or advance the slot clock depend on this initialization. Writing at `simulation_id` as key establishes the isolation boundary — each simulation run owns exactly one slot clock record.

Last-write-wins semantics apply: re-initializing the same `simulation_id` resets the slot clock. Callers are responsible for ensuring this is invoked exactly once per simulation run.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; primary isolation key; becomes the slot clock record key |
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
| SUCCESS | Slot clock record written successfully |
| VIOLATION | Invalid input (empty simulation_id) |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION on empty or invalid `simulation_id` key
- BACKEND_ERROR if the SLOT_CLOCK store is unavailable
- No ALREADY_EXISTS — CS_MUTABLE_JSON_V0 WRITE is last-write-wins

---

## Machine

```yaml
cc_code: CC_INITIALIZE_SLOT_CLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Initialize slot clock record for a simulation run

  inputs:
    simulation_id:
      type: string
      required: true
      description: Primary isolation key; becomes the slot clock record key
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
    - step: write_slot_clock_init
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: SLOT_CLOCK
      op: WRITE
      inputs:
        key: $.inputs.simulation_id
        value:
          simulation_id: $.inputs.simulation_id
          current_slot: 0
          initialized_at: "{{timestamp}}"
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
    - SLOT_CLOCK store is defined in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
    - keyed by simulation_id — isolation invariant established at init
    - last-write-wins; callers must ensure single init per simulation run
```
