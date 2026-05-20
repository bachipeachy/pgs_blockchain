# RB_SUBMIT_TRANSACTION_V0

## Header (Mandatory)

- **Artifact Code:** RB_SUBMIT_TRANSACTION_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## Machine

```yaml
rb_code: RB_SUBMIT_TRANSACTION_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for transaction submission workflow
  description: Binds capability side effects to concrete runtime implementations for transaction submission.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy:
        path: "{{module_data_root}}/blockchain/identity/registry/actors.json"

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy:
        path: "{{module_data_root}}/blockchain/transaction/events/transaction_events.jsonl"

    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
```