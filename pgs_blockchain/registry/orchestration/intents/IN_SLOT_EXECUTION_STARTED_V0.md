# IN_SLOT_EXECUTION_STARTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_SLOT_EXECUTION_STARTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_PROCESS_SLOT_V0

---

## 1. Intent

Admit a single slot execution request. Declares the simulation identity and slot number to be processed by `WF_PROCESS_SLOT_V0`.

---

## 2. Rationale

Each slot execution is an atomic unit: one `simulation_id` + one `slot_number` → one slot clock read → one block proposal. Declaring both at admission ensures the slot identity is established before the CC pipeline begins; no dynamic slot computation occurs inside the WF.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_PROCESS_SLOT_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; must be non-empty; scopes the slot clock read |
| `slot_number` | integer | true | Global slot counter value to process; must be >= 0 |
| `triggered_by` | string | true | Actor ID or system trigger reference; must be non-empty |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Slot execution intent accepted; proceed to WF_PROCESS_SLOT_V0 |
| NACK | Intent rejected — invalid or missing required fields |

---

## 6. Domain

- **Domain:** pgs.blockchain.orchestration
- **Subdomain:** orchestration
- **Authority:** SYSTEM

---

## Machine

```yaml
in_code: IN_SLOT_EXECUTION_STARTED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Admit single slot execution request
  workflow: WF_PROCESS_SLOT_V0

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; scopes the slot clock read
    slot_number:
      type: integer
      required: true
      description: Global slot counter value to process; must be >= 0
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outcomes:
    ACK:
      description: Slot execution intent accepted
    NACK:
      description: Intent rejected — invalid or missing required fields

extensions:
  domain: pgs.blockchain.orchestration
  subdomain: orchestration
  authority: SYSTEM
```
