# RB_RUN_CHAIN_SIMULATION_V0

## Header (Mandatory)

- **Artifact Code:** RB_RUN_CHAIN_SIMULATION_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the chain simulation coordination workflow. Binds CS_MUTABLE_JSON_V0 for slot clock initialization (CC_INITIALIZE_SLOT_CLOCK_V0), CS_APPENDONLY_JSONL_V0 for simulation summary recording (CC_RECORD_SIMULATION_SUMMARY_V0), and CS_CONCURRENT_WORKFLOWS_V0 for concurrent worker dispatch (CC_DISPATCH_SIMULATION_WORKERS_V0).

---

## 2. Scope

Supports:

- CS_MUTABLE_JSON_V0 for SLOT_CLOCK store WRITE (CC_INITIALIZE_SLOT_CLOCK_V0)
- CS_APPENDONLY_JSONL_V0 for SIMULATION_SUMMARY store APPEND (CC_RECORD_SIMULATION_SUMMARY_V0)
- CS_CONCURRENT_WORKFLOWS_V0 for EXECUTE_CONCURRENT dispatch of consensus loop and TX workload workers (CC_DISPATCH_SIMULATION_WORKERS_V0)

All store paths are declared in STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0 and resolved at runtime via the `store:` field in each CC step. Dispatched sub-WFs carry their own runtime bindings. No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_RUN_CHAIN_SIMULATION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for chain simulation coordination workflow
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_ORCHESTRATION_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}
    capability_side_effects::CS_CONCURRENT_WORKFLOWS_V0:
      policy: {}
```
