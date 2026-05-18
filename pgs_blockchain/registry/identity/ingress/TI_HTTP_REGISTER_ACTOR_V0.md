# TI_HTTP_REGISTER_ACTOR_V0

## Machine

```yaml
artifact_code: TI_HTTP_REGISTER_ACTOR_V0
artifact_type: TI
artifact_kind: intent
version: 0

governed_by:
  - fb.transport::CONSTITUTION_TRANSPORT_V0

core:
  summary: HTTP ingress for actor registration
  description: >
    Declares the HTTP transport ingress point for actor registration.
    Defines the route, admission schema, and explicit workflow binding.

  route:
    method: POST
    path: /api/v0/register_actor
    content_type: application/json

  admission_schema:
    actor_record:
      type: object
      required: true

  workflow: blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0

  outcomes:
    ACK:
      description: Actor record accepted for registration workflow
    NACK:
      description: Actor record rejected at admission
```

---

## Purpose

Declares the HTTP transport ingress point for actor registration.

Governs the boundary between the external HTTP client and
`blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0`. Transport ends at admission.

## Route

| Field | Value |
|-------|-------|
| Method | POST |
| Path | /api/v0/register_actor |
| Content-Type | application/json |

## Admission Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| actor_record | object | yes | Proposed actor registration payload |
