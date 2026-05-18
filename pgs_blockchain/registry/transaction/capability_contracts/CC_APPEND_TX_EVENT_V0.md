# CC_APPEND_TX_EVENT_V0

## Header (Mandatory)

- **Artifact Code:** CC_APPEND_TX_EVENT_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Append a transaction lifecycle event to the transaction event journal.

---

## 2. Rationale

Transaction events provide an observable, append-only trail of transaction
lifecycle transitions. Events are emitted after successful persistence.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_APPENDONLY_JSONL_V0 | CS | APPEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| event_type | string | true | Event code (e.g., EV_TRANSACTION_SUBMITTED_V0) |
| tx_id | string | true | Transaction identifier |
| tx_hash | string | true | Transaction hash |
| wallet_id | string | true | Source wallet |
| actor_id | string | true | Submitting actor |
| data | object | true | Event-specific payload |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | SUCCESS, VIOLATION, or BACKEND_ERROR |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Event appended |
| VIOLATION | Invalid event data |
| BACKEND_ERROR | Storage write failure |

---

## Machine

```yaml
cc_code: CC_APPEND_TX_EVENT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Append transaction lifecycle event

  inputs:
    event_type:
      type: string
      required: true
    tx_id:
      type: string
      required: true
    tx_hash:
      type: string
      required: true
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    data:
      type: object
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]

  pipeline:
    - step: append_tx_event
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: TRANSACTION_EVENTS
      op: APPEND
      inputs:
        stream_id: $.inputs.tx_id
        actor_id: $.inputs.actor_id
        record:
          event_code: $.inputs.event_type
          tx_id: $.inputs.tx_id
          tx_hash: $.inputs.tx_hash
          wallet_id: $.inputs.wallet_id
          payload: $.inputs.data
          timestamp: "{{timestamp}}"
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
