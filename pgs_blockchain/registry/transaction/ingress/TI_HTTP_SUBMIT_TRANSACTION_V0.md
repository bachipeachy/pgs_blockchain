# TI_HTTP_SUBMIT_TRANSACTION_V0

## Machine

```yaml
artifact_code: TI_HTTP_SUBMIT_TRANSACTION_V0
artifact_type: TI
artifact_kind: intent
version: 0

governed_by:
  - fb.transport::CONSTITUTION_TRANSPORT_V0

core:
  summary: HTTP ingress for transaction submission
  description: >
    Declares the HTTP ingress point for transaction submission.
    Defines the route, method, admission schema, and explicit workflow binding.

  route:
    method: POST
    path: /api/v0/submit_transaction
    content_type: application/json

  admission_schema:
    actor_record:
      type: object
      required: true
    wallet_id:
      type: string
      required: true
    to_address:
      type: string
      required: true
      pattern: "^0x[0-9a-fA-F]{40}$"
    value:
      type: string
      required: true
    mnemonic:
      type: string
      required: true

  workflow: blockchain::WF_SUBMIT_TRANSACTION_V0

  outcomes:
    ACK:
      description: Request structurally valid, forwarded to workflow
    NACK:
      description: Request structurally invalid, rejected at admission
```

---

## Purpose

Declares the HTTP transport ingress point for transaction submission.

This artifact governs the boundary between the external HTTP client and the
`blockchain::WF_SUBMIT_TRANSACTION_V0` workflow. It defines:
- The HTTP route and method
- The admission schema (normalized canonical envelope fields)
- The explicit, static workflow binding

Transport ends at admission. Execution semantics are entirely owned by the
bound workflow.

## Route

| Field | Value |
|-------|-------|
| Method | POST |
| Path | /api/v0/submit_transaction |
| Content-Type | application/json |

## Admission Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| actor_record | object | yes | Actor identity record |
| wallet_id | string | yes | Wallet identifier |
| to_address | string | yes | Ethereum address (0x + 40 hex chars) |
| value | string | yes | Transaction value |
| mnemonic | string | yes | Wallet mnemonic |

## Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Request structurally valid, forwarded to workflow |
| NACK | Request structurally invalid, rejected at admission |
