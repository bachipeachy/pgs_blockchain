# AC_SYSTEM_V0

## Header (Mandatory)

- **Artifact Code:** AC_SYSTEM_V0
- **Artifact Kind:** actor
- **Governed By:** CONSTITUTION_GOVERNANCE_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Identity

A system authority actor represents a system process or administrator with elevated privileges.

---

## 2. Rationale

System actors represent non-human authorities:
- Perform administrative actions
- Act as verifiers in verification workflows
- Provide audit trail for system-initiated operations

---

## 3. Type

| Property | Value |
|----------|-------|
| Type | system |

---

## 4. Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| role | string | true | System role identifier |
| permissions | array of strings | false | Declared capabilities (descriptive only) |

---

## Machine

```yaml
ac_code: AC_SYSTEM_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  summary: System Authority Actor
  description: Represents a layers process or administrator with elevated privileges
  type: layers

  attributes:
    role:
      type: string
      required: true
    permissions:
      type: array
      items:
        type: string
```
