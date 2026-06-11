# RB_STAKE_V0

## Header (Mandatory)

- **Artifact Code:** RB_STAKE_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## Machine

```yaml
rb_code: RB_STAKE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for STAKE transaction workflow
  description: Binds capability side effects to concrete runtime implementations for STAKE (ENDUSER). Includes actor registry for ownership check.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy:
        path: "{{module_data_root}}/blockchain/identity/registry/actors.json"

    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}
```
