# EV_GENESIS_CREATED_V0

## Header (Mandatory)

- **Artifact Code:** EV_GENESIS_CREATED_V0
- **Artifact Kind:** event
- **Governed By:** CONSTITUTION_EVENT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** NONE

---

## 1. Fact

Announce that the genesis chain was created

---

## 2. Emitted By

- `blockchain::CC_CREATE_GENESIS_BLOCK_V0`

---

## 3. Schema

| Field | Type | Required | Format | Description |
|-------|------|----------|--------|-------------|
| genesis_hash | string | true |  | Genesis block content hash |
| height | integer | true |  | Block height (0 for genesis) |
| timestamp | string | true | date-time | When genesis was created |

---

## Machine

```yaml
ev_code: EV_GENESIS_CREATED_V0
version: v0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0
core:
  summary: Announce that the genesis chain was created
  description: Announce that the genesis chain was created
  schema:
    genesis_hash:
      type: string
      required: true
    height:
      type: integer
      required: true
    timestamp:
      type: string
      required: true
      format: date-time
```
