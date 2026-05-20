# WF_REGISTER_ACTOR_UNVERIFIED_V0

## Header (Mandatory)

- **Artifact Code:** WF_REGISTER_ACTOR_UNVERIFIED_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_ACTOR_REGISTERED_V0, CC_GENERATE_ACTOR_ID_V0, CC_REGISTER_ACTOR_KYC_V0, CC_APPEND_ACTOR_EVENT_V0

---

## 1. Intent

Register a new actor in an unverified state, creating their identity record and emitting a registration event.

---

## 2. Rationale

Actor registration is the entry point for identity management:
- Generates deterministic actor ID from record
- Registers actor in KYC system
- Emits event for downstream verification workflow

---

## 3. Execution Graph

```
IN_ACTOR_REGISTERED_V0
    ├─ ACK → CC_GENERATE_ACTOR_ID_V0
    │           ├─ SUCCESS → CC_REGISTER_ACTOR_KYC_V0
    │           │               ├─ SUCCESS → CC_APPEND_ACTOR_EVENT_V0 → EXIT
    │           │               ├─ ALREADY_EXISTS → CC_APPEND_ACTOR_EVENT_V0 → EXIT
    │           │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           └─ VIOLATION → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_ACTOR_REGISTERED_V0 | IN | Entry intent for actor registration |
| CC_GENERATE_ACTOR_ID_V0 | CC | Generate deterministic actor ID |
| CC_REGISTER_ACTOR_KYC_V0 | CC | Register actor in KYC system |
| CC_APPEND_ACTOR_EVENT_V0 | CC | Emit registration event |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

No admission requirements - this is an open registration workflow.

---

## Machine

```yaml
wf_code: WF_REGISTER_ACTOR_UNVERIFIED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0

runtime_binding: blockchain::RB_REGISTER_ACTOR_UNVERIFIED_V0
subdomain: identity

core:
  summary: Register an unverified actor
  start_node: IN_ACTOR_REGISTERED_V0

  nodes:
    IN_ACTOR_REGISTERED_V0:
      type: IN
      code: IN_ACTOR_REGISTERED_V0
      next:
        ACK: CC_GENERATE_ACTOR_ID_V0
        NACK: EXIT

    CC_GENERATE_ACTOR_ID_V0:
      type: CC
      code: CC_GENERATE_ACTOR_ID_V0
      inputs:
        actor_record: $.payload.actor_record
      next:
        SUCCESS: CC_REGISTER_ACTOR_KYC_V0
        VIOLATION: EXIT

    CC_REGISTER_ACTOR_KYC_V0:
      type: CC
      code: CC_REGISTER_ACTOR_KYC_V0
      inputs:
        actor_record: $.payload.actor_record
        actor_id: $.results.CC_GENERATE_ACTOR_ID_V0.actor_id
      next:
        SUCCESS: CC_APPEND_ACTOR_EVENT_V0
        ALREADY_EXISTS: CC_APPEND_ACTOR_EVENT_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_APPEND_ACTOR_EVENT_V0:
      type: CC
      code: CC_APPEND_ACTOR_EVENT_V0
      inputs:
        event_type: EV_ACTOR_REGISTERED_UNVERIFIED_V0
        actor_id: $.results.CC_GENERATE_ACTOR_ID_V0.actor_id
        data: $.payload.actor_record
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT:
      type: EXIT
      reason: EXITED
```
