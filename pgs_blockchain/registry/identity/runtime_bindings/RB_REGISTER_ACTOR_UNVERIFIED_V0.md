# RB_REGISTER_ACTOR_UNVERIFIED_V0

## Header (Mandatory)

- **Artifact Code:** RB_REGISTER_ACTOR_UNVERIFIED_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## 1. Intent

Provide runtime bindings required to execute the actor registration workflow for unverified actors.

---

## 2. Scope

Supports:

- Registry binding for KYC lookup
- Append-only event logging

No additional capabilities permitted.

---

## Machine

```yaml
rb_code: RB_REGISTER_ACTOR_UNVERIFIED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for actor registration workflow
  description: Binds capability side effects to concrete runtime implementations for actor registration.
  storage_structure: blockchain::STRUCTURE_BLOCKCHAIN_STORAGE_V0

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy:
        path: "{{module_data_root}}/blockchain/identity/registry/actors.json"

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy: {}
```