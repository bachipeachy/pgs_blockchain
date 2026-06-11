# RB_RUN_TX_WORKLOAD_V0

## Header (Mandatory)

- **Artifact Code:** RB_RUN_TX_WORKLOAD_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the TX workload coordination workflow. Binds CS_WORKFLOW_LOOP_V0 for the Collatz TX sequence loop within CC_RUN_TX_SEQUENCE_V0.

---

## 2. Scope

Supports:

- CS_WORKFLOW_LOOP_V0 for EXECUTE_SEQUENCE operations (Collatz TX loop absorbed inside CC_RUN_TX_SEQUENCE_V0)

All store paths are declared in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. Invoked WFs (typed TX WFs — WF_MINT_V0, WF_TRANSFER_V0, etc.) carry their own runtime bindings. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_RUN_TX_WORKLOAD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for TX workload coordination workflow
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0

  bindings:
    capability_side_effects::CS_WORKFLOW_LOOP_V0:
      policy: {}
```
