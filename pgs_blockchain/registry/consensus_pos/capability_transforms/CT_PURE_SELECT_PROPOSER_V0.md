# CT_PURE_SELECT_PROPOSER_V0

## Header (Mandatory)

- **Artifact Code:** CT_PURE_SELECT_PROPOSER_V0
- **Artifact Kind:** atom
- **Governed By:** CONSTITUTION_CAPABILITY_TRANSFORMS_V0
- **Version:** v0
- **Supersedes:** NONE
- **Dependencies:** NONE (pure deterministic selection)

---

## Human

### 1. Intent

Select the block proposer for a given consensus round from the set of eligible validators.

---

### 2. Rationale

Proposer selection is a pure deterministic function of round number and eligible validator set. It carries no side effects and no external state. Isolating it here means future algorithm changes (e.g. weighted stake selection) require only a new CT version — no CC, WF, or CS changes.

---

### 3. Naming Convention

- **Artifact Code:** CT_PURE_SELECT_PROPOSER_V0
- **Operation:** SELECT_PROPOSER

---

### 4. Applicability & Non-Applicability

#### 4.1 Valid Use Cases

- Selecting the proposer for a PoS consensus round
- Deterministic round-robin proposer rotation

#### 4.2 Invalid Use Cases

- Weighted or staked selection (requires a new CT version)
- Any selection involving randomness or external state

---

### 5. Determinism & Purity Declaration

| Property | Value | Notes |
|--------|------|------|
| Deterministic | YES | Same inputs always yield same proposer_id |
| Purity Class | ct_pure | No state, no side effects |
| Side Effects | NONE | Pure selection transform |
| Replay Safe | YES | Deterministic mapping |

---

### 6. Structural Checklist

- [x] Single responsibility
- [x] Deterministic
- [x] No implicit state
- [x] Inputs fully declared
- [x] Outputs fully declared
- [x] Fail-loud on invalid input

---

### 7. Composition Rules

As an **atom**, this CT:
- MUST NOT invoke other CTs
- MUST perform exactly one transformation
- MAY be composed by molecules

---

### 8. Validation Expectations

**Runtime validation MUST fail (VIOLATION) if:**
- `eligible_validators` is empty
- `round_number` is negative

---

### 9. Observability

This atom does NOT emit domain events.

---

### 10. Security Considerations

- Proposer selection is deterministic and publicly verifiable
- This atom does not persist any state

---

### 11. Minimal Usage Shape

{eligible_validators, round_number} → CT_PURE_SELECT_PROPOSER_V0 → proposer_id

---

## Machine

```yaml
ct_code: CT_PURE_SELECT_PROPOSER_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Select block proposer for a consensus round
  description: Deterministic round-robin selection of proposer from eligible validators using round_number modulo
  inputs:
    eligible_validators:
      type: array
      required: true
      description: "Array of active validator records; each must have actor_id field"
    round_number:
      type: integer
      required: true
      description: "Non-negative consensus round number"
  outputs:
    proposer_id:
      type: string
      description: "actor_id of the selected proposer"

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: SELECT_PROPOSER
  implementation:
    module: pgs_blockchain.implementation.capability_transforms.atoms.ct_pure_select_proposer_v0
    callable: execute
```
