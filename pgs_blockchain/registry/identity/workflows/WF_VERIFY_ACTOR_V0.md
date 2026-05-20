# WF_VERIFY_ACTOR_V0

## Header (Mandatory)

- **Artifact Code:** WF_VERIFY_ACTOR_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_ACTOR_VERIFIED_V0, CC_RESOLVE_ACTOR_ID_V0, CC_RECORD_ACTOR_STATE_V0, CC_APPEND_ACTOR_EVENT_V0, CC_PERSIST_VERIFIED_ACTOR_V0

---

## 1. Intent

Process a verification decision for an actor, transitioning from unverified to verified state and persisting the result.

---

## 2. Rationale

Actor verification is a governance checkpoint:
- Requires prior registration (admission control)
- Records state transition with audit trail
- Persists verified actor for downstream workflows

---

## 3. Execution Graph

```
IN_ACTOR_VERIFIED_V0
    ├─ ACK → CC_RESOLVE_ACTOR_ID_V0
    │           ├─ SUCCESS → CC_RECORD_ACTOR_STATE_V0
    │           │               ├─ SUCCESS → CC_APPEND_ACTOR_EVENT_V0
    │           │               │               ├─ SUCCESS → CC_PERSIST_VERIFIED_ACTOR_V0 → EXIT
    │           │               │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           └─ NOT_FOUND/VIOLATION → EXIT
    └─ NACK → EXIT
```

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_ACTOR_VERIFIED_V0 | IN | Entry intent for verification decision |
| CC_RESOLVE_ACTOR_ID_V0 | CC | Resolve actor_record to actor_id |
| CC_RECORD_ACTOR_STATE_V0 | CC | Record state transition |
| CC_APPEND_ACTOR_EVENT_V0 | CC | Emit verification event |
| CC_PERSIST_VERIFIED_ACTOR_V0 | CC | Persist verified actor record |
| EXIT | EXIT | Terminal node |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | EV_ACTOR_REGISTERED_UNVERIFIED_V0 |

Actor must be registered. Re-runs are permitted; downstream nodes handle idempotent exits.

---

## Machine

```yaml
wf_code: WF_VERIFY_ACTOR_V0
version: V0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_VERIFY_ACTOR_V0
subdomain: identity

core:
  runtime_binding: blockchain::RB_VERIFY_ACTOR_V0
  summary: Process actor verification decision

  admission:
    requires:
      - EV_ACTOR_REGISTERED_UNVERIFIED_V0
    bindings:
      EV_ACTOR_REGISTERED_UNVERIFIED_V0:
        actor_id: actor_id

  start_node: IN_ACTOR_VERIFIED_V0

  nodes:
    IN_ACTOR_VERIFIED_V0:
      type: IN
      code: IN_ACTOR_VERIFIED_V0
      next:
        ACK: CC_RESOLVE_ACTOR_ID_V0
        NACK: EXIT

    CC_RESOLVE_ACTOR_ID_V0:
      type: CC
      code: CC_RESOLVE_ACTOR_ID_V0
      inputs:
        actor_record: $.payload.actor_record
      next:
        SUCCESS: CC_RECORD_ACTOR_STATE_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT

    CC_RECORD_ACTOR_STATE_V0:
      type: CC
      code: CC_RECORD_ACTOR_STATE_V0
      inputs:
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        old_state: UNVERIFIED
        new_state: $.payload.decision
        reason: $.payload.notes
        timestamp: "2025-01-01T00:00:00Z"
      next:
        SUCCESS: CC_APPEND_ACTOR_EVENT_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_APPEND_ACTOR_EVENT_V0:
      type: CC
      code: CC_APPEND_ACTOR_EVENT_V0
      inputs:
        event_type: EV_ACTOR_VERIFIED_V0
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        data:
          verifier_id: $.payload.verifier_id
          decision: $.payload.decision
          notes: $.payload.notes
      next:
        SUCCESS: CC_PERSIST_VERIFIED_ACTOR_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_PERSIST_VERIFIED_ACTOR_V0:
      type: CC
      code: CC_PERSIST_VERIFIED_ACTOR_V0
      inputs:
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        target_cs: CS_APPENDONLY_JSONL_V0
        target_ref: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
      next:
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT
        ALREADY_EXISTS: EXIT

    EXIT:
      type: EXIT
      reason: EXITED
```
