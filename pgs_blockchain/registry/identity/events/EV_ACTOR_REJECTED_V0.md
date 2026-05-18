# EV_ACTOR_REJECTED_V0

## Header (Mandatory)

- **Artifact Code:** EV_ACTOR_REJECTED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An actor verification has been rejected by a system authority.

---

## 2. Rationale

This event records verification rejection:
- Captures rejection reason for audit
- Prevents downstream workflows from proceeding
- Provides compliance trail

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_VERIFY_ACTOR_V0 | CC_APPEND_ACTOR_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Unique identifier of the rejected actor |
| verifier_id | string | true | ID of the system authority that rejected |
| rejection_reason | string | true | Reason for rejection |
| timestamp | string (date-time) | true | When rejection occurred |

---

## Machine

```yaml
ev_code: EV_ACTOR_REJECTED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Actor Rejected
  description: Emitted when an actor verification fails

  schema:
    actor_id:
      type: string
      required: true
    verifier_id:
      type: string
      required: true
    rejection_reason:
      type: string
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
