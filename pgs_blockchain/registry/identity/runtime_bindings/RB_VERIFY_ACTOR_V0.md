# RB_VERIFY_ACTOR_V0

## Header (Mandatory)

- **Artifact Code:** RB_VERIFY_ACTOR_V0
- **Artifact Kind:** runtime_binding
- **Governed By:** CONSTITUTION_RUNTIME_BINDING_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE

---

## Machine

```yaml
rb_code: RB_VERIFY_ACTOR_V0
version: v0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: Runtime binding for actor verification workflow
  description: Binds capability side effects to concrete runtime implementations for actor verification.

  bindings:
    capability_side_effects::CS_REGISTRY_V0:
      policy:
        path: "{{module_data_root}}/blockchain/identity/registry/actors.json"

    capability_side_effects::CS_APPENDONLY_JSONL_V0:
      policy:
        path: "{{module_data_root}}/blockchain/identity/events/identity_events.jsonl"
```