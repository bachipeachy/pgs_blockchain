# IN_RUN_CHAIN_SIMULATION_V0

## Header (Mandatory)

- **Artifact Code:** IN_RUN_CHAIN_SIMULATION_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_RUN_CHAIN_SIMULATION_V0

---

## 1. Intent

Admit a chain simulation run request. Declares the simulation identity, slot schedule, TX workload, and all parameters needed to launch a fully governed simulation via `WF_RUN_CHAIN_SIMULATION_V0`.

---

## 2. Rationale

`simulation_id` is the primary isolation boundary — every slot clock record and simulation summary is keyed by it. Declaring it at admission ensures the isolation invariant is established before any state is written.

`tx_sequence` carries fully resolved TX payload objects. The intent validates structure at admission; individual TX field validity is enforced within each targeted TX workflow.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_RUN_CHAIN_SIMULATION_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `simulation_id` | string | true | Primary isolation key; must be non-empty; scopes all slot clock and simulation summary records |
| `slot_duration_seconds` | integer | true | Duration of each slot in seconds; must be > 0 |
| `max_slots` | integer | true | Total number of slots to execute; must be >= 1 |
| `tx_interval_seconds` | integer | true | Interval between TX workload submissions in seconds; must be > 0 |
| `max_transactions` | integer | true | Maximum number of transactions to submit; must be >= 1 |
| `tx_sequence` | array | true | Non-empty; each item must carry `tx_type` and all required payload fields for the targeted TX workflow |
| `triggered_by` | string | true | Actor ID or system trigger reference; must be non-empty |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Chain simulation intent accepted; proceed to WF_RUN_CHAIN_SIMULATION_V0 |
| NACK | Intent rejected — invalid or missing required fields |

---

## 6. Domain

- **Domain:** pgs.blockchain.orchestration
- **Subdomain:** orchestration
- **Authority:** SYSTEM

---

## Machine

```yaml
in_code: IN_RUN_CHAIN_SIMULATION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Admit chain simulation run request
  workflow: WF_RUN_CHAIN_SIMULATION_V0

  inputs:
    simulation_id:
      type: string
      required: true
      description: Primary isolation key; scopes all slot clock and simulation summary records
    slot_duration_seconds:
      type: integer
      required: true
      description: Duration of each slot in seconds; must be > 0
    max_slots:
      type: integer
      required: true
      description: Total number of slots to execute; must be >= 1
    tx_interval_seconds:
      type: integer
      required: true
      description: Interval between TX workload submissions in seconds; must be > 0
    max_transactions:
      type: integer
      required: true
      description: Maximum number of transactions to submit; must be >= 1
    tx_sequence:
      type: array
      required: true
      description: Non-empty list of TX specs; each item carries tx_type and all required payload fields for the targeted TX workflow
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outcomes:
    ACK:
      description: Chain simulation intent accepted
    NACK:
      description: Intent rejected — invalid or missing required fields

extensions:
  domain: pgs.blockchain.orchestration
  subdomain: orchestration
  authority: SYSTEM
```
