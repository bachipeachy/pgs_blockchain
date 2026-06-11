# WF_CREATE_WALLET_V0

## Header (Mandatory)

- **Artifact Code:** WF_CREATE_WALLET_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** IN_WALLET_CREATED_V0, CC_RESOLVE_ACTOR_ID_V0, CC_GENERATE_WALLET_ID_V0, CC_CHECK_WALLET_EXISTS_V0, CC_DERIVE_WALLET_KEYS_V0, CC_CREATE_WALLET_RECORD_V0, CC_APPEND_WALLET_EVENT_V0, CC_NOTIFY_WALLET_CREATED_V0

---

## 1. Intent

Create a wallet for a verified actor, establishing their financial account with HD-derived cryptographic addresses.

---

## 2. Rationale

Wallet creation requires:
- Actor must be verified (admission control)
- Wallet ID is deterministically generated
- Existence check gates crypto derivation (no wasted entropy for duplicates)
- HD key derivation produces EOA and UTXO addresses from a single seed
- Wallet record is persisted with event trail
- Email notification is best-effort (failure does not cascade)

---

## 3. Execution Graph

```
IN_WALLET_CREATED_V0
    ├─ ACK → CC_RESOLVE_ACTOR_ID_V0
    │           ├─ SUCCESS → CC_GENERATE_WALLET_ID_V0
    │           │           ├─ SUCCESS → CC_CHECK_WALLET_EXISTS_V0
    │           │               ├─ NOT_FOUND → CC_DERIVE_WALLET_KEYS_V0
    │           │               │               ├─ SUCCESS → CC_CREATE_WALLET_RECORD_V0
    │           │               │               │               ├─ SUCCESS → CC_APPEND_WALLET_EVENT_V0
    │           │               │               │               │               ├─ SUCCESS → CC_NOTIFY_WALLET_CREATED_V0
    │           │               │               │               │               │               ├─ SUCCESS → EXIT
    │           │               │               │               │               │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           │               │               │               │               │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           │               │               │               │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           │               │               │               └─ ALREADY_EXISTS/VIOLATION/BACKEND_ERROR → EXIT
    │           │               │               └─ VIOLATION → EXIT
    │           │               ├─ SUCCESS → EXIT (wallet already exists)
    │           │               └─ VIOLATION/BACKEND_ERROR → EXIT
    │           │           └─ VIOLATION → EXIT
    │           └─ NOT_FOUND/VIOLATION → EXIT
    └─ NACK → EXIT
```

**Ordering invariant:** CC_DERIVE_WALLET_KEYS_V0 executes only after CC_CHECK_WALLET_EXISTS_V0 confirms NOT_FOUND (wallet is new). No crypto work is performed for duplicate wallet requests.

**Notification semantics:** CC_NOTIFY_WALLET_CREATED_V0 failure routes to EXIT, terminating the workflow. Email is required.

---

## 4. Nodes

| Node | Type | Purpose |
|------|------|---------|
| IN_WALLET_CREATED_V0 | IN | Entry intent for wallet creation |
| CC_RESOLVE_ACTOR_ID_V0 | CC | Resolve actor_record to actor_id |
| CC_GENERATE_WALLET_ID_V0 | CC | Generate deterministic wallet ID |
| CC_CHECK_WALLET_EXISTS_V0 | CC | Gate: check wallet does not already exist |
| CC_DERIVE_WALLET_KEYS_V0 | CC | Derive EOA + UTXO keypairs via HD path |
| CC_CREATE_WALLET_RECORD_V0 | CC | Assemble and persist wallet record |
| CC_APPEND_WALLET_EVENT_V0 | CC | Emit wallet created event |
| CC_NOTIFY_WALLET_CREATED_V0 | CC | Send wallet creation notification email |
| EXIT | EXIT | Terminal node (failure / early exit) |
| EXIT_SUCCESS | EXIT | Terminal node (successful wallet creation) |

---

## 5. Admission

| Requirement | Description |
|-------------|-------------|
| requires | EV_ACTOR_VERIFIED_V0 |

Actor must be verified before wallet creation.

---

## Machine

```yaml
wf_code: WF_CREATE_WALLET_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_CREATE_WALLET_V0
subdomain: wallet

core:
  runtime_binding: blockchain::RB_CREATE_WALLET_V0
  summary: Create wallet with HD-derived addresses for verified actor

  admission:
    requires:
      - EV_ACTOR_VERIFIED_V0
    forbids: []
    bindings:
      EV_ACTOR_VERIFIED_V0:
        actor_id: actor_id

  start_node: IN_WALLET_CREATED_V0

  nodes:
    IN_WALLET_CREATED_V0:
      type: IN
      code: IN_WALLET_CREATED_V0
      next:
        ACK: CC_RESOLVE_ACTOR_ID_V0
        NACK: EXIT

    CC_RESOLVE_ACTOR_ID_V0:
      type: CC
      code: CC_RESOLVE_ACTOR_ID_V0
      inputs:
        actor_record: $.payload.actor_record
      next:
        SUCCESS: CC_GENERATE_WALLET_ID_V0
        NOT_FOUND: EXIT
        VIOLATION: EXIT

    CC_GENERATE_WALLET_ID_V0:
      type: CC
      code: CC_GENERATE_WALLET_ID_V0
      inputs:
        seed_record:
          actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
          type: wallet
          wallet_type: $.payload.wallet_type
      next:
        SUCCESS: CC_CHECK_WALLET_EXISTS_V0
        VIOLATION: EXIT

    CC_CHECK_WALLET_EXISTS_V0:
      type: CC
      code: CC_CHECK_WALLET_EXISTS_V0
      inputs:
        wallet_id: $.results.CC_GENERATE_WALLET_ID_V0.wallet_id
      next:
        NOT_FOUND: CC_DERIVE_WALLET_KEYS_V0
        SUCCESS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_DERIVE_WALLET_KEYS_V0:
      type: CC
      code: CC_DERIVE_WALLET_KEYS_V0
      inputs:
        coin_type: 66
      next:
        SUCCESS: CC_CREATE_WALLET_RECORD_V0
        VIOLATION: EXIT

    CC_CREATE_WALLET_RECORD_V0:
      type: CC
      code: CC_CREATE_WALLET_RECORD_V0
      inputs:
        wallet_id: $.results.CC_GENERATE_WALLET_ID_V0.wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        wallet_type: $.payload.wallet_type
        currency: $.payload.wallet_config.currency
        network: $.payload.wallet_config.metadata.network
        security_type: $.payload.wallet_config.metadata.security_type
        eoa_public_key_hex: $.results.CC_DERIVE_WALLET_KEYS_V0.eoa_public_key_hex
        eoa_address: $.results.CC_DERIVE_WALLET_KEYS_V0.eoa_address
        eoa_derivation_path: $.results.CC_DERIVE_WALLET_KEYS_V0.eoa_derivation_path
        utxo_public_key_hex: $.results.CC_DERIVE_WALLET_KEYS_V0.utxo_public_key_hex
        utxo_address: $.results.CC_DERIVE_WALLET_KEYS_V0.utxo_address
        utxo_derivation_path: $.results.CC_DERIVE_WALLET_KEYS_V0.utxo_derivation_path
        master_fingerprint: $.results.CC_DERIVE_WALLET_KEYS_V0.master_fingerprint
        email_registration: $.payload.actor_record.email_registration
      next:
        SUCCESS: CC_APPEND_WALLET_EVENT_V0
        ALREADY_EXISTS: EXIT
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_APPEND_WALLET_EVENT_V0:
      type: CC
      code: CC_APPEND_WALLET_EVENT_V0
      inputs:
        wallet_id: $.results.CC_GENERATE_WALLET_ID_V0.wallet_id
        actor_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
        record:
          event_type: EV_WALLET_CREATED_V0
          wallet_id: $.results.CC_GENERATE_WALLET_ID_V0.wallet_id
          owner_id: $.results.CC_RESOLVE_ACTOR_ID_V0.actor_id
          wallet_type: $.payload.wallet_type
          wallet_config: $.payload.wallet_config
      next:
        SUCCESS: CC_NOTIFY_WALLET_CREATED_V0
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    CC_NOTIFY_WALLET_CREATED_V0:
      type: CC
      code: CC_NOTIFY_WALLET_CREATED_V0
      inputs:
        recipient_email: $.payload.actor_record.email_registration
        wallet_id: $.results.CC_GENERATE_WALLET_ID_V0.wallet_id
        wallet_type: $.payload.wallet_type
      next:
        SUCCESS: EXIT_SUCCESS
        VIOLATION: EXIT
        BACKEND_ERROR: EXIT

    EXIT_SUCCESS:
      type: EXIT
      reason: COMPLETED

    EXIT:
      type: EXIT
      reason: EXITED
```
