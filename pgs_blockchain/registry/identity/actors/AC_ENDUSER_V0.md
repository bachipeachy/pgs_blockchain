# AC_ENDUSER_V0

## Header (Mandatory)

- **Artifact Code:** AC_ENDUSER_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

An end-user actor represents a human user interacting with the system.

---

## 2. Rationale

End-user actors are the primary participants in the system:
- Represent human identities
- Track KYC verification status
- Provide natural key attributes for resolution

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | person |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | true | User's email address |
| first_name | string | true | User's first name |
| last_name | string | true | User's last name |
| kyc_status | string (enum) | false | Verification status: UNVERIFIED, VERIFIED, REJECTED |

---

## Machine

```yaml
ac_code: AC_ENDUSER_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: End-User Actor
  description: Represents a human user interacting with the layers
  type: person

  attributes:
    email:
      type: string
      required: true
    first_name:
      type: string
      required: true
    last_name:
      type: string
      required: true
    kyc_status:
      type: string
      enum:
        - UNVERIFIED
        - VERIFIED
        - REJECTED
      default: UNVERIFIED
```
