# IN_BOOTSTRAP_GENESIS_CHAIN_V0

## Header (Mandatory)

- **Artifact Code:** IN_BOOTSTRAP_GENESIS_CHAIN_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** WF_BOOTSTRAP_GENESIS_CHAIN_V0

---

## 1. Intent

Admit a request to bootstrap the genesis chain and initialise the supply.

---

## 2. Rationale



---

## 3. Workflow Binding

| Target | Description |
|---|---|
| WF_BOOTSTRAP_GENESIS_CHAIN_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|---|---|---|---|
| genesis_block_content | object | true |  |

---

## 5. Outcomes

| Outcome | Description |
|---|---|
| ACK |  |
| NACK |  |

---

## Machine

```yaml
in_code: IN_BOOTSTRAP_GENESIS_CHAIN_V0
version: v0
governed_by: fb.topology::CONSTITUTION_INTENT_V0
core:
  summary: Admit a request to bootstrap the genesis chain and initialise the supply.
  workflow: WF_BOOTSTRAP_GENESIS_CHAIN_V0
  inputs:
    genesis_block_content:
      type: object
      required: true
  outcomes:
    ACK:
      description: ''
    NACK:
      description: ''
```
