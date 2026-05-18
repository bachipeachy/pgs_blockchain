# CC_APPEND_WALLET_EVENT_V0

## Header (Mandatory)

- **Artifact Code:** CC_APPEND_WALLET_EVENT_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Append a wallet lifecycle event to the wallet event journal.

---

## 2. Rationale

Wallet events require:
- Immutable event log
- Event sourcing capability
- Audit trail for wallet lifecycle

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| wallet_id | string | true | Wallet identifier (used as stream_id) |
| actor_id | string | true | Actor performing the event |
| record | object | true | Pre-assembled event record payload |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Event appended successfully |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR
- APPEND is not idempotent; retries create duplicates

---

## Machine

```yaml
cc_code: CC_APPEND_WALLET_EVENT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Append wallet lifecycle event

  inputs:
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    record:
      type: object
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: append_wallet_event
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: WALLET_EVENTS
      op: APPEND
      inputs:
        record: $.inputs.record
        stream_id: $.inputs.wallet_id
        actor_id: $.inputs.actor_id
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
