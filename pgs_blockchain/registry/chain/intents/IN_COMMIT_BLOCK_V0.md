# IN_COMMIT_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** IN_COMMIT_BLOCK_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_COMMIT_BLOCK_V0

---

## 1. Intent

Admit a request to commit a proposed block to the canonical chain.

---

## 2. Rationale



---

## 3. Workflow Binding

| Target | Description |
|---|---|
| WF_COMMIT_BLOCK_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|---|---|---|---|
| proposed_block | object | true |  |

---

## 5. Outcomes

| Outcome | Description |
|---|---|
| ACK |  |
| NACK |  |

---

## Machine

```yaml
in_code: IN_COMMIT_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0
core:
  summary: Admit a request to commit a proposed block to the canonical chain.
  workflow: WF_COMMIT_BLOCK_V0
  inputs:
    proposed_block:
      type: object
      required: true
  outcomes:
    ACK:
      description: ''
    NACK:
      description: ''
```
