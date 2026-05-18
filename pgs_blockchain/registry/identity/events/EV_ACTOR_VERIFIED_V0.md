# EV_ACTOR_VERIFIED_V0

## Header (Mandatory)

- **Artifact Code:** EV_ACTOR_VERIFIED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An actor has been successfully verified by a system authority.

---

## 2. Rationale

This event marks actor verification completion:
- Records verifier identity and decision
- Enables downstream workflows (e.g., wallet creation)
- Provides audit trail for compliance

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_VERIFY_ACTOR_V0 | CC_APPEND_ACTOR_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Unique identifier of the verified actor |
| verifier_id | string | true | ID of the system authority that verified |
| verification_notes | string | false | Optional notes from verifier |
| timestamp | string (date-time) | true | When verification occurred |

---

## Machine

```yaml
ev_code: EV_ACTOR_VERIFIED_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Actor Verified
  description: Emitted when an actor is successfully verified by a layers authority

  schema:
    actor_id:
      type: string
      required: true
    verifier_id:
      type: string
      required: true
    verification_notes:
      type: string
    timestamp:
      type: string
      format: date-time
      required: true
```
