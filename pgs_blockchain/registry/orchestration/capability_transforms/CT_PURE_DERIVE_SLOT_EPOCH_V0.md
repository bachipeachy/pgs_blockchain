# CT_PURE_DERIVE_SLOT_EPOCH_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_DERIVE_SLOT_EPOCH_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## Human

### 1. Intent

Derive slot context fields (`slot_index`, `epoch_number`, `round_number`, `timestamp`) from a globally-increasing slot number and slot start timestamp. Pure computation — zero side effects, zero CS calls.

Used by `CC_PREPARE_SLOT_CONTEXT_V0` to transform raw slot clock state into the richer context needed for block proposal and slot execution routing.

---

### 2. Determinism & Purity Declaration

| Property | Value | Notes |
|----------|-------|-------|
| Deterministic | YES | Same inputs yield identical outputs |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure arithmetic transform |
| Replay Safe | YES | Deterministic mapping |
| CS Calls | NONE | CT purity invariant — CT may never call CS |

---

### 3. Field Naming Precision

| Field | Semantics |
|-------|-----------|
| `slot_number` | Globally-increasing counter; never resets; passed in from slot clock |
| `slot_index` | Intra-epoch position (0-based); resets to 0 at each epoch boundary |
| `epoch_number` | Monotonically increasing epoch counter |
| `round_number` | Pass-through of `slot_number`; satisfies `WF_PROPOSE_BLOCK_V0` payload contract |
| `timestamp` | Pass-through of `slot_start_ts`; carries clock read result forward |

`slot_index` and `slot_number` are semantically distinct — use exact field names throughout.

---

## Machine

```yaml
ct_code: CT_PURE_DERIVE_SLOT_EPOCH_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Derive slot_index, epoch_number, round_number, and timestamp from slot_number and slot_start_ts
  description: Pure arithmetic transform; maps globally-increasing slot counter to intra-epoch position, epoch number, block proposal round, and timestamp
  inputs:
    slot_number:
      type: integer
      required: true
    slot_start_ts:
      type: string
      required: false
      default: null
      description: Slot start timestamp; when omitted, a deterministic ISO timestamp is derived from slot_number (base 2026-01-01T00:00:00Z + slot × 30 s)
    slots_per_epoch:
      type: integer
      required: false
      default: 32
  outputs:
    round_number:
      type: integer
    slot_index:
      type: integer
    epoch_number:
      type: integer
    timestamp:
      type: string

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: DERIVE_SLOT_EPOCH
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_derive_slot_epoch_v0
    callable: execute
```
