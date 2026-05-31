# EV_VALIDATOR_REGISTERED_V0

## Header (Mandatory)

- **Artifact Code:** EV_VALIDATOR_REGISTERED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

An actor has been successfully registered as a validator node in the consensus layer.

---

## 2. Rationale

This event marks the entry point of the validator lifecycle:
- Records that validator registration occurred
- Captures the full validator record at the moment of registration
- Provides audit trail for validator onboarding and consensus participation history

---

## 3. Emitted By

| Workflow | Capability Contract |
|----------|---------------------|
| WF_REGISTER_VALIDATOR_V0 | CC_APPEND_VALIDATOR_EVENT_V0 |

---

## 4. Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_id | string | true | PGS actor ID of the registered validator |
| validator_record | object | true | Full validator registration payload at time of registration |
| timestamp | string (date-time) | true | When validator registration occurred |

---

## Machine

```yaml
ev_code: EV_VALIDATOR_REGISTERED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Validator Registered
  description: Emitted when an actor is successfully registered as a validator node

  schema:
    actor_id:
      type: string
      required: true
    validator_record:
      type: object
      required: true
    timestamp:
      type: string
      format: date-time
      required: true
```
