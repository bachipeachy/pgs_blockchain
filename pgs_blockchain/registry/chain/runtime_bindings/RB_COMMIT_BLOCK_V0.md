# RB_COMMIT_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** RB_COMMIT_BLOCK_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## Machine

```yaml
rb_code: RB_COMMIT_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0
core:
  summary: Bind the commit workflow to its stores
  storage_structure: blockchain::STRUCTURE_CHAIN_STORAGE_V0
  bindings:
    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}
    capability_side_effects::CS_MUTABLE_JSON_V0:
      policy: {}
```
