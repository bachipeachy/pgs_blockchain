# IN_CONSENSUS_LOOP_STARTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_CONSENSUS_LOOP_STARTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_RUN_CONSENSUS_LOOP_V0

---

## 1. Intent

Admit a consensus loop execution request. Declares the simulation identity and the ordered slot schedule to be executed by `WF_RUN_CONSENSUS_LOOP_V0`.

---

## 2. Rationale

`slot_schedule` is the pre-resolved list of slot numbers to process in order. Declaring it at admission gives the WF a deterministic, governed iteration target without requiring the runtime to compute slot ranges dynamically.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_RUN_CONSENSUS_LOOP_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Simulation run identifier; must be non-empty; used to scope slot clock reads and writes |
| `slot_schedule` | array | true | Non-empty ordered list of integer slot numbers (>= 0) to execute |
| `triggered_by` | string | true | Actor ID or system trigger reference; must be non-empty |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Consensus loop intent accepted; proceed to WF_RUN_CONSENSUS_LOOP_V0 |
| NACK | Intent rejected — invalid or missing required fields |

---

## 6. Domain

- **Domain:** pgs.blockchain.orchestration
- **Subdomain:** orchestration
- **Authority:** SYSTEM

---

## Machine

```yaml
in_code: IN_CONSENSUS_LOOP_STARTED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Admit consensus loop execution request
  workflow: WF_RUN_CONSENSUS_LOOP_V0

  inputs:
    simulation_id:
      type: string
      required: true
      description: Simulation run identifier; scopes slot clock reads and writes
    slot_schedule:
      type: array
      required: true
      description: Non-empty ordered list of integer slot numbers (>= 0) to execute
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outcomes:
    ACK:
      description: Consensus loop intent accepted
    NACK:
      description: Intent rejected — invalid or missing required fields

extensions:
  domain: pgs.blockchain.orchestration
  subdomain: orchestration
  authority: SYSTEM
```
