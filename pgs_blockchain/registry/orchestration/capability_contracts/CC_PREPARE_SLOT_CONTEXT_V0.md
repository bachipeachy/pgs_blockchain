# CC_PREPARE_SLOT_CONTEXT_V0

## Header (Mandatory)

- **Artifact Code:** CC_PREPARE_SLOT_CONTEXT_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_DERIVE_SLOT_EPOCH_V0

---

## 1. Intent

Derive the full slot execution context from a raw slot number. Invokes `CT_PURE_DERIVE_SLOT_EPOCH_V0` to compute `slot_index`, `epoch_number`, `round_number`, and `timestamp` from `slot_number` and `slot_start_ts`.

---

## 2. Rationale

Block proposal and slot routing require richer context than the raw `slot_number` provided by the slot clock. This CC is the single point where slot clock state is transformed into execution context. The CT is pure — no side effects, deterministic output for identical inputs.

`slot_start_ts` is optional — when not supplied, the CT derives a deterministic ISO timestamp from `slot_number` (base epoch `2026-01-01T00:00:00Z` + slot × 30 s). `slots_per_epoch` defaults to 32 and is optional — the protocol constant governs epoch boundaries.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_DERIVE_SLOT_EPOCH_V0 | CT | DERIVE_SLOT_EPOCH |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slot_number` | integer | true | Global slot counter value; sourced from slot clock `current_slot` via upstream CC_READ_SLOT_CLOCK_V0 |
| `slots_per_epoch` | integer | false | Epoch boundary divisor; default 32 |
| `triggered_by` | string | true | Actor ID or system trigger reference |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `slot_index` | integer | Intra-epoch slot position (0-based); `slot_number % slots_per_epoch` |
| `epoch_number` | integer | Monotonically increasing epoch counter; `slot_number // slots_per_epoch` |
| `round_number` | integer | Pass-through of `slot_number`; satisfies WF_PROPOSE_BLOCK_V0 payload contract |
| `timestamp` | string | Slot start timestamp; captured at context preparation time |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Slot context derived successfully |
| VIOLATION | Invalid input (negative slot_number, invalid slots_per_epoch) |

---

## 7. Failure Semantics

- VIOLATION on invalid `slot_number` (negative or non-integer) or `slots_per_epoch < 1`
- CT is pure — no storage, no network; BACKEND_ERROR is not applicable

---

## Machine

```yaml
cc_code: CC_PREPARE_SLOT_CONTEXT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Derive slot execution context via CT_PURE_DERIVE_SLOT_EPOCH_V0

  inputs:
    slot_number:
      type: integer
      required: true
      description: Global slot counter; sourced from slot clock current_slot
    slots_per_epoch:
      type: integer
      required: false
      default: 32
      description: Epoch boundary divisor; protocol constant
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string
    slot_index:
      type: integer
    epoch_number:
      type: integer
    round_number:
      type: integer
    timestamp:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]
    on_input_failure: VIOLATION

  pipeline:
    - step: derive_slot_epoch
      transform: blockchain::CT_PURE_DERIVE_SLOT_EPOCH_V0
      op: DERIVE_SLOT_EPOCH
      inputs:
        slot_number: $.inputs.slot_number
        slots_per_epoch: $.inputs.slots_per_epoch
      outputs:
        slot_index: $.capability_result.slot_index
        epoch_number: $.capability_result.epoch_number
        round_number: $.capability_result.round_number
        timestamp: $.capability_result.timestamp
      on_ct_result:
        on_success: SUCCESS
        on_failure: VIOLATION
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: exit
        VIOLATION: exit

extensions:
  subdomain: orchestration
  notes:
    - slot_start_ts omitted — CT derives deterministic ISO timestamp from slot_number when not supplied
    - slots_per_epoch defaults to 32 if not supplied; CT applies same default
    - slot_index and slot_number are semantically distinct; use exact field names downstream
    - round_number is a pass-through of slot_number; satisfies WF_PROPOSE_BLOCK_V0 contract
```
