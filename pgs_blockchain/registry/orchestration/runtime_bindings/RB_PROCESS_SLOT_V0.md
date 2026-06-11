# RB_PROCESS_SLOT_V0

## Header (Mandatory)

- **Artifact Code:** RB_PROCESS_SLOT_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the single slot processing workflow. Binds CS_MUTABLE_JSON_V0 for slot clock reads and advances, and CS_WORKFLOW_GATEWAY_V0 for block proposal invocation via CC_INVOKE_BLOCK_PROPOSAL_V0.

---

## 2. Scope

Supports:

- CS_MUTABLE_JSON_V0 for SLOT_CLOCK store READ (CC_READ_SLOT_CLOCK_V0) and WRITE (CC_ADVANCE_SLOT_CLOCK_V0)
- CS_WORKFLOW_GATEWAY_V0 for EXECUTE invocation of WF_PROPOSE_BLOCK_V0 (CC_INVOKE_BLOCK_PROPOSAL_V0)

All store paths are declared in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. Invoked WFs (WF_PROPOSE_BLOCK_V0) carry their own runtime bindings. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_PROCESS_SLOT_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for single slot execution workflow
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
    capability_side_effects::CS_WORKFLOW_GATEWAY_V0:
      policy: {}
```
