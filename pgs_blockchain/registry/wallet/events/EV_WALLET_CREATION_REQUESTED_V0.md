# EV_WALLET_CREATION_REQUESTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_WALLET_CREATION_REQUESTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

A wallet creation has been requested for a verified actor.

---

## 2. Rationale

This event records wallet creation initiation:
- Links wallet request to actor identity
- Provides request tracking via request_id
- Enables audit of wallet lifecycle

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_CREATE_WALLET_V0 | CC_APPEND_WALLET_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Owner of the requested wallet |
| request_id | string | true | Unique identifier for this request |
| timestamp | string (date-time) | true | When request occurred |

---

## Machine

```yaml
ev_code: EV_WALLET_CREATION_REQUESTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Wallet Creation Requested
  description: Emitted to trigger wallet creation for a verified actor

  schema:
    actor_id:
      type: string
      required: true
    request_id:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
