# IN_ACTOR_VERIFIED_V0

## Header (Mandatory)

- **Artifact Code:** IN_ACTOR_VERIFIED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_VERIFY_ACTOR_V0

---

## 1. Intent

Record a verification decision for an actor, transitioning from unverified to verified or rejected state.

---

## 2. Rationale

Actor verification is a governance checkpoint:
- Requires explicit decision (VERIFIED or REJECTED)
- Requires verifier authority identification
- Creates immutable audit trail

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_VERIFY_ACTOR_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor identity data (first_name, last_name, email_registration) |
| verifier_id | string | true | ID of the system authority performing verification |
| decision | string (enum) | true | Verification decision: VERIFIED or REJECTED |
| notes | string | false | Optional verification notes |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Verification decision recorded |
| NACK | Verification failed |

---

## 6. Domain

- **Domain:** pgs.identity.actor

---

## Machine

```yaml
in_code: IN_ACTOR_VERIFIED_V0
version: V0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Verify an actor
  workflow: WF_VERIFY_ACTOR_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Actor identity data (first_name, last_name, email_registration)
    verifier_id:
      type: string
      required: true
      description: ID of the layers authority performing verification
    decision:
      type: string
      enum:
        - VERIFIED
        - REJECTED
      required: true
      description: Verification decision
    notes:
      type: string
      description: Optional verification notes

  outcomes:
    ACK:
      description: Verification decision recorded
    NACK:
      description: Verification failed

extensions:
  domain: pgs.identity.actor
```
