# IN_ACTOR_REGISTERED_V0

## Header (Mandatory)

- **Artifact Code:** IN_ACTOR_REGISTERED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_REGISTER_ACTOR_UNVERIFIED_V0

---

## 1. Intent

Register a new actor in an unverified state, initiating the actor onboarding process.

---

## 2. Rationale

Actor registration is the entry point for identity management:
- Captures proposed actor data
- Creates an unverified actor record
- Triggers subsequent verification workflow via event

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_REGISTER_ACTOR_UNVERIFIED_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Proposed actor registration payload |
| actor_record.first_name | string | true | Actor first name |
| actor_record.last_name | string | true | Actor last name |
| actor_record.email_registration | string | true | Actor email (format: email) |
| actor_record.currency_preference | string | false | Preferred currency (default: BACHI) |
| actor_record.language | string | false | Preferred language code (default: en) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Actor record accepted for verification |
| NACK | Actor record rejected |

---

## 6. Domain

- **Domain:** pgs.identity.actor
- **Notes:**
  - Initiates the actor onboarding process
  - Result is an unverified actor record
  - Triggers verification workflow via event

---

## Machine

```yaml
in_code: IN_ACTOR_REGISTERED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Register a new actor (Unverified)
  workflow: WF_REGISTER_ACTOR_UNVERIFIED_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Proposed actor registration payload
      fields:
        first_name:
          type: string
          required: true
        last_name:
          type: string
          required: true
        email_registration:
          type: string
          required: true
          format: email
        currency_preference:
          type: string
          required: false
          default: BACHI
          description: Preferred currency
        language:
          type: string
          required: false
          default: en
          description: Preferred language code

  outcomes:
    ACK:
      description: Actor record accepted for verification
    NACK:
      description: Actor record rejected

extensions:
  domain: pgs.identity.actor
  notes:
    - Initiates the actor onboarding process
    - Result is an unverified actor record
    - Triggers verification workflow via event
```
