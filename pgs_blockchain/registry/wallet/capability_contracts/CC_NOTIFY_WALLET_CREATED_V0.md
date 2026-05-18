# CC_NOTIFY_WALLET_CREATED_V0

## Header (Mandatory)

- **Artifact Code:** CC_NOTIFY_WALLET_CREATED_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_SEND_EMAIL_V0

---

## 1. Intent

Send wallet creation notification email to the wallet owner.

---

## 2. Rationale

Post-creation notification:
- Confirms wallet creation to the actor via email
- Best-effort delivery — failure does not cascade to workflow failure
- Non-structural: email is informational, not part of the wallet creation contract

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_SEND_EMAIL_V0 | CS | SEND |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| recipient_email | string | true | Recipient email address |
| wallet_id | string | true | Wallet identifier for notification content |
| wallet_type | string | true | Wallet type for notification content |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Email sent or skipped (testbed-safe) |
| VIOLATION | Invalid input (e.g., missing email address) |
| BACKEND_ERROR | SMTP connection failure |

---

## 7. Failure Semantics

- **Non-structural.** Email failure does NOT cascade to workflow failure.
- BACKEND_ERROR maps to `exit` (not `fail`) — workflow transitions to EXIT with SUCCESS status.
- Does NOT emit a StructuredError with structural error_code.
- Does NOT rethrow exceptions as structural failures.
- SMTP unavailable or skipped results in `delivery_status: "skipped"` with SUCCESS.

This is the first CC in the wallet domain that tolerates failure — exercises the BUSINESS_VIOLATION vs structural distinction.

---

## Machine

```yaml
cc_code: CC_NOTIFY_WALLET_CREATED_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Send wallet creation notification email

  inputs:
    recipient_email:
      type: string
      required: true
    wallet_id:
      type: string
      required: true
    wallet_type:
      type: string
      required: true

  outputs:
    result_status:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: send_wallet_notification
      side_effect: capability_side_effects::CS_SEND_EMAIL_V0
      op: SEND
      inputs:
        recipient: $.inputs.recipient_email
        subject: "Wallet Created"
        body: "Your wallet has been created successfully."
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
