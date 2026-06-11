# CC_READ_SLOT_CLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CC_READ_SLOT_CLOCK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0

---

## 1. Intent

Read the current slot clock record for a simulation run. Returns the full slot clock record keyed by `simulation_id`. NOT_FOUND is a hard failure — slot clock must be initialized before any slot processing begins.

---

## 2. Rationale

The slot clock is the authoritative state for slot sequencing. Any CC that needs the current slot position reads it via this CC. Treating NOT_FOUND as a hard exit (rather than a recoverable state) enforces the invariant that `CC_INITIALIZE_SLOT_CLOCK_V0` must succeed before any slot processing CC is invoked.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | READ |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; scopes the slot clock read |
| `triggered_by` | string | true | Actor ID or system trigger reference |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `slot_clock` | object | Full slot clock record: `{simulation_id, current_slot, initialized_at}` |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Slot clock record found and returned |
| NOT_FOUND | No slot clock record exists for this simulation_id — hard exit |
| VIOLATION | Invalid input (empty simulation_id) |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- NOT_FOUND is a hard exit — no slot clock means the simulation was not initialized; caller must not proceed
- VIOLATION on empty or invalid `simulation_id` key
- BACKEND_ERROR if the SLOT_CLOCK store is unavailable

---

## Machine

```yaml
cc_code: CC_READ_SLOT_CLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Read current slot clock record for a simulation run

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; scopes the slot clock read
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string
    slot_clock:
      type: object
      description: Full slot clock record

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
        result_status: $.capability_result.result_status
        slot_clock: $.capability_result.value
      result_surface: [SUCCESS, NOT_FOUND, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        NOT_FOUND: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - SLOT_CLOCK store is defined in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0
    - NOT_FOUND is a hard failure — slot clock must be initialized before slot processing
    - slot_clock output carries full record including current_slot
```
