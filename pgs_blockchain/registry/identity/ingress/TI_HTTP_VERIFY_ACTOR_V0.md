# TI_HTTP_VERIFY_ACTOR_V0

## Machine

```yaml
artifact_code: TI_HTTP_VERIFY_ACTOR_V0
artifact_type: TI
artifact_kind: intent
version: 0

governed_by:
  - fb.transport::CONSTITUTION_TRANSPORT_V0

core:
  summary: HTTP ingress for actor verification
  description: >
    Declares the HTTP transport ingress point for actor verification.
    Defines the route, admission schema, and explicit workflow binding.

  route:
    method: POST
    path: /api/v0/verify_actor
    content_type: application/json

  admission_schema:
    actor_record:
      type: object
      required: true
    verifier_id:
      type: string
      required: true
    decision:
      type: string
      required: true
    notes:
      type: string
      required: false

  workflow: blockchain::WF_VERIFY_ACTOR_V0

  outcomes:
    ACK:
      description: Verification decision accepted and forwarded to workflow
    NACK:
      description: Verification request rejected at admission
```

---

## Purpose

Declares the HTTP transport ingress point for actor verification.

Governs the boundary between the external HTTP client and
`blockchain::WF_VERIFY_ACTOR_V0`. Transport ends at admission.

## Route

| Field | Value |
|-------|-------|
| Method | POST |
| Path | /api/v0/verify_actor |
| Content-Type | application/json |

## Admission Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| actor_record | object | yes | Actor identity data |
| verifier_id | string | yes | ID of the authority performing verification |
| decision | string | yes | VERIFIED or REJECTED |
| notes | string | no | Optional verification notes |
