# EV_TRANSACTION_REJECTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_TRANSACTION_REJECTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A transaction has been rejected during validation.

---

## 2. Rationale

This event records transaction rejection:
- Captures the error code and reason
- Links rejection to wallet for audit
- Enables observability of failure patterns

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_SUBMIT_TRANSACTION_V0 | CC_APPEND_TX_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tx_id | string | false | Transaction identifier (may not exist if rejected early) |
| wallet_id | string | true | Source wallet |
| error_code | string | true | Structured error code |
| reason | string | true | Human-readable rejection reason |
| timestamp | string (date-time) | true | When rejection occurred |

---

## Machine

```yaml
ev_code: EV_TRANSACTION_REJECTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Transaction rejected during validation
  description: Emitted when a transaction fails structural, policy, or signing validation

  schema:
    tx_id:
      type: string
    wallet_id:
      type: string
      required: true
    error_code:
      type: string
      required: true
    reason:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
