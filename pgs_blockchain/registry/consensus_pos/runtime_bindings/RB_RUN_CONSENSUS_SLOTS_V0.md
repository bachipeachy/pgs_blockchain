# RB_RUN_CONSENSUS_SLOTS_V0

## Header (Mandatory)

- **Artifact Code:** RB_RUN_CONSENSUS_SLOTS_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the consensus slot run workflow. Binds CS_WORKFLOW_LOOP_V0 for the Collatz slot loop within CC_EXECUTE_SLOT_SEQUENCE_V0, and CS_MUTABLE_JSON_V0 for store reads in CC_VERIFY_SLOT_RESULTS_V0.

---

## 2. Scope

Supports:

- CS_WORKFLOW_LOOP_V0 for EXECUTE_SEQUENCE operations (Collatz slot loop absorbed inside CC_EXECUTE_SLOT_SEQUENCE_V0)
- CS_MUTABLE_JSON_V0 for BLOCKS and TRANSACTION store LIST reads in CC_VERIFY_SLOT_RESULTS_V0

All store paths are declared in STRUCTURE_BLOCKCHAIN_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. Invoked WFs (WF_PROPOSE_BLOCK_V0, typed tx WFs) carry their own runtime bindings. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_RUN_CONSENSUS_SLOTS_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for consensus slot run workflow
  description: Binds CS_WORKFLOW_LOOP_V0 for the Collatz slot loop and CS_MUTABLE_JSON_V0 for post-run store assertion reads. All store paths resolved from STRUCTURE_BLOCKCHAIN_STORAGE_V0.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_WORKFLOW_LOOP_V0:
      policy: {}

    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
```