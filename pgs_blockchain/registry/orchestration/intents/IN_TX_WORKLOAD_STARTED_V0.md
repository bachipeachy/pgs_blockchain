# IN_TX_WORKLOAD_STARTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_TX_WORKLOAD_STARTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_RUN_TX_WORKLOAD_V0

---

## 1. Intent

Admit a TX workload execution request. Declares the transaction interval and the ordered sequence of typed TX submissions to be dispatched by `WF_RUN_TX_WORKLOAD_V0`.

---

## 2. Rationale

`tx_sequence` carries fully resolved TX payload objects — each item declares `tx_type` and all fields required by the targeted TX workflow. Resolving payloads at admission ensures the workload is self-contained; no payload construction logic is needed inside the WF.

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_RUN_TX_WORKLOAD_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tx_interval_seconds` | integer | true | Interval between TX submissions in seconds; must be > 0 |
| `tx_sequence` | array | true | Non-empty ordered list of TX specs; each item carries `tx_type` and all required payload fields for the targeted TX workflow |
| `triggered_by` | string | true | Actor ID or system trigger reference; must be non-empty |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | TX workload intent accepted; proceed to WF_RUN_TX_WORKLOAD_V0 |
| NACK | Intent rejected — invalid or missing required fields |

---

## 6. Domain

- **Domain:** pgs.blockchain.orchestration
- **Subdomain:** orchestration
- **Authority:** SYSTEM

---

## Machine

```yaml
in_code: IN_TX_WORKLOAD_STARTED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Admit TX workload execution request
  workflow: WF_RUN_TX_WORKLOAD_V0

  inputs:
    tx_interval_seconds:
      type: integer
      required: true
      description: Interval between TX submissions in seconds; must be > 0
    tx_sequence:
      type: array
      required: true
      description: Non-empty ordered list of TX specs; each item carries tx_type and all required payload fields for the targeted TX workflow
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outcomes:
    ACK:
      description: TX workload intent accepted
    NACK:
      description: Intent rejected — invalid or missing required fields

extensions:
  domain: pgs.blockchain.orchestration
  subdomain: orchestration
  authority: SYSTEM
```
