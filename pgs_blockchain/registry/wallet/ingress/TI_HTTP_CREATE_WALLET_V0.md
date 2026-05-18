# TI_HTTP_CREATE_WALLET_V0

## Machine

```yaml
artifact_code: TI_HTTP_CREATE_WALLET_V0
artifact_type: TI
artifact_kind: intent
version: 0

governed_by:
  - fb.transport::CONSTITUTION_TRANSPORT_V0

core:
  summary: HTTP ingress for wallet creation
  description: >
    Declares the HTTP transport ingress point for wallet creation.
    Defines the route, admission schema, and explicit workflow binding.

  route:
    method: POST
    path: /api/v0/create_wallet
    content_type: application/json

  admission_schema:
    actor_record:
      type: object
      required: true
    wallet_type:
      type: string
      required: false
    wallet_config:
      type: object
      required: false

  workflow: blockchain::WF_CREATE_WALLET_V0

  outcomes:
    ACK:
      description: Wallet creation request accepted and forwarded to workflow
    NACK:
      description: Wallet creation request rejected at admission
```

---

## Purpose

Declares the HTTP transport ingress point for wallet creation.

Governs the boundary between the external HTTP client and
`blockchain::WF_CREATE_WALLET_V0`. Transport ends at admission.

## Route

| Field | Value |
|-------|-------|
| Method | POST |
| Path | /api/v0/create_wallet |
| Content-Type | application/json |

## Admission Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| actor_record | object | yes | Actor identity data |
| wallet_type | string | no | Type of wallet (default: standard) |
| wallet_config | object | no | Optional wallet configuration |
