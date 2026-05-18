# EV_ACTOR_REGISTERED_UNVERIFIED_V0

## Header (Mandatory)

- **Artifact Code:** EV_ACTOR_REGISTERED_UNVERIFIED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An actor has been registered in the system but has not yet undergone verification.

---

## 2. Rationale

This event marks the entry point of the actor lifecycle:
- Records that registration occurred
- Enables downstream verification workflow admission
- Provides audit trail for actor onboarding

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_REGISTER_ACTOR_UNVERIFIED_V0 | CC_APPEND_ACTOR_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | Unique identifier of the registered actor |
| registration_data | object | true | Actor registration payload |
| timestamp | string (date-time) | true | When registration occurred |

---

## Machine

```yaml
ev_code: EV_ACTOR_REGISTERED_UNVERIFIED_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Actor Registered (Unverified)
  description: Emitted when a new actor registers but has not yet been verified

  schema:
    actor_id:
      type: string
      required: true
    registration_data:
      type: object
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
