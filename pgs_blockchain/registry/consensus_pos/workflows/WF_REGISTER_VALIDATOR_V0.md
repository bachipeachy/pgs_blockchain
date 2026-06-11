# WF_REGISTER_VALIDATOR_V0

## Header (Mandatory)

- **Artifact Code:** WF_REGISTER_VALIDATOR_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** IN_VALIDATOR_REGISTERED_V0, CC_CHECK_ACTOR_EXISTS_V0, CC_CHECK_VALIDATOR_EXISTS_V0, CC_WRITE_VALIDATOR_RECORD_V0, CC_APPEND_VALIDATOR_EVENT_V0

---

## 1. Intent

Register an existing actor as a validator node — enforces the actor prerequisite gate, prevents duplicate registration, writes the validator record, and emits a lifecycle event.

---

## 2. Rationale

Validator registration requires sequential enforcement:
- Actor must exist in the identity registry before being admitted as a validator (cross-subdomain prerequisite gate)
- Duplicate registration must be rejected (one actor, one validator record)
- Registration event must be appended to the append-only journal for audit and observability

The VALIDATOR store uses CS_MUTABLE_JSON_V0 (not CS_REGISTRY_V0) so that the RB can bind
CS_REGISTRY_V0 exclusively to the ACTOR store (required by CC_CHECK_ACTOR_EXISTS_V0). A single
CS FQDN maps to one policy in the RB — using two CS_REGISTRY_V0 bindings with different paths
in the same workflow is not expressible. Duplicate detection is handled by CC_CHECK_VALIDATOR_EXISTS_V0
(CS_MUTABLE_JSON_V0 GET → NOT_FOUND / SUCCESS routing) before the write step.

---

## 3. Execution Graph

```
IN_VALIDATOR_REGISTERED_V0
    ├─ ACK → CC_CHECK_ACTOR_EXISTS_V0
    │           ├─ SUCCESS → CC_CHECK_VALIDATOR_EXISTS_V0
    │           │               ├─ NOT_FOUND → CC_WRITE_VALIDATOR_RECORD_V0
    │           │               │                  ├─ SUCCESS → CC_APPEND_VALIDATOR_EVENT_V0 → EXIT
    │           │               │                  ├─ VIOLATION → EXIT
    │           │               │                  └─ BACKEND_ERROR → EXIT
    │           │               ├─ SUCCESS → EXIT  (already registered)
    │           │               ├─ VIOLATION → EXIT
    │           │               └─ BACKEND_ERROR → EXIT
    │           └─ NOT_FOUND/VIOLATION/BACKEND_ERROR → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_VALIDATOR_REGISTERED_V0 | IN | Entry intent — validates payload |
| CC_CHECK_ACTOR_EXISTS_V0 | CC | Actor prerequisite gate (cross-subdomain, identity) |
| CC_CHECK_VALIDATOR_EXISTS_V0 | CC | Duplicate detection — VALIDATOR store existence check |
| CC_WRITE_VALIDATOR_RECORD_V0 | CC | Write validator record to VALIDATOR store |
| CC_APPEND_VALIDATOR_EVENT_V0 | CC | Emit validator registration lifecycle event |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

Actor must already be registered in the identity registry. This is enforced by CC_CHECK_ACTOR_EXISTS_V0 as the first execution node after ACK.

---

## Machine

```yaml
wf_code: WF_REGISTER_VALIDATOR_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_REGISTER_VALIDATOR_V0
subdomain: consensus_pos

core:
  summary: Register an actor as a validator node
  start_node: IN_VALIDATOR_REGISTERED_V0

  nodes:
    IN_VALIDATOR_REGISTERED_V0:
      type: IN
      code: IN_VALIDATOR_REGISTERED_V0
      next:
        ACK: CC_CHECK_ACTOR_EXISTS_V0
        NACK: EXIT

    CC_CHECK_ACTOR_EXISTS_V0:
      type: CC
      code: CC_CHECK_ACTOR_EXISTS_V0
      inputs:
        actor_id: $.payload.validator_record.actor_id
      next:
        SUCCESS: CC_CHECK_VALIDATOR_EXISTS_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_CHECK_VALIDATOR_EXISTS_V0:
      type: CC
      code: CC_CHECK_VALIDATOR_EXISTS_V0
      inputs:
        actor_id: $.payload.validator_record.actor_id
      next:
        NOT_FOUND: CC_WRITE_VALIDATOR_RECORD_V0
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_WRITE_VALIDATOR_RECORD_V0:
      type: CC
      code: CC_WRITE_VALIDATOR_RECORD_V0
      inputs:
        validator_record: $.payload.validator_record
      next:
        SUCCESS: CC_APPEND_VALIDATOR_EVENT_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_APPEND_VALIDATOR_EVENT_V0:
      type: CC
      code: CC_APPEND_VALIDATOR_EVENT_V0
      inputs:
        event_type: EV_VALIDATOR_REGISTERED_V0
        actor_id: $.payload.validator_record.actor_id
        data: $.payload.validator_record
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED
```
