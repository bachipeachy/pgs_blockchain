# CC_ADVANCE_SLOT_CLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CC_ADVANCE_SLOT_CLOCK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Advance the slot clock by one position. Reads the current slot clock record, increments `current_slot` by 1, and writes the updated record back to the SLOT_CLOCK store.

---

## 2. Rationale

The slot clock tracks the simulation's position in the slot sequence. After each slot completes its full pipeline (block proposal included), the clock must be advanced before the next slot iteration is dispatched. The increment is CC-implementation-level arithmetic (not delegated to a CT) — `current_slot + 1` is the only computation.

The 2-step READ → WRITE pattern is deliberate: the CC reads the authoritative record before writing, ensuring no external state assumption is made about the current slot value.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ |
| 2 | CS_MUTABLE_JSON_V0 | CS | WRITE |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; scopes both the READ and WRITE |
| `triggered_by` | string | true | Actor ID or system trigger reference |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `next_slot` | integer | The new `current_slot` value written to the store (`previous + 1`) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Slot clock advanced and written successfully |
| NOT_FOUND | Slot clock record not found — simulation not initialized |
| VIOLATION | Invalid input or malformed slot clock record |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- NOT_FOUND on READ exits immediately — slot clock must exist before it can be advanced
- VIOLATION on invalid `simulation_id` or malformed record exits
- BACKEND_ERROR on READ or WRITE exits; partial writes are not possible across two steps if the READ fails

---

## Machine

```yaml
cc_code: CC_ADVANCE_SLOT_CLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Advance slot clock current_slot by 1 — READ then WRITE

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; scopes the slot clock READ and WRITE
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string
    next_slot:
      type: integer
      description: The new current_slot value written (previous + 1)

  result_status_contract:
    allowed: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: read_slot_clock
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: SLOT_CLOCK
      op: READ
      inputs:
        key: $.inputs.simulation_id
      outputs:
        current_slot_record: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: write_advanced_slot_clock
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: SLOT_CLOCK
      op: WRITE
      inputs:
        key: $.inputs.simulation_id
        value:
          simulation_id: $.inputs.simulation_id
          current_slot: "{{$.results.read_slot_clock.current_slot_record.current_slot + 1}}"
          initialized_at: $.results.read_slot_clock.current_slot_record.initialized_at
          last_advanced_at: "{{timestamp}}"
      outputs:
        result_status: $.capability_result.result_status
        next_slot: "{{$.results.read_slot_clock.current_slot_record.current_slot + 1}}"
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - SLOT_CLOCK store is defined in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
    - CC-level arithmetic — current_slot + 1; no CT required
    - 2-step READ then WRITE; NOT_FOUND on READ is a hard exit
    - next_slot output = the value written, available for downstream CC JSONPath resolution
```
