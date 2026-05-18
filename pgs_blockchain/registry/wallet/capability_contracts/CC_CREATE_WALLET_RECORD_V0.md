# CC_CREATE_WALLET_RECORD_V0

## Header (Mandatory)

- **Artifact Code:** CC_CREATE_WALLET_RECORD_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_MUTABLE_JSON_V0, CS_REGISTRY_V0

---

## 1. Intent

Assemble a complete V0 wallet record from upstream CC outputs and payload data, persist the full record to CS_MUTABLE_JSON_V0, then register a pointer in CS_REGISTRY_V0.

---

## 2. Rationale

Wallet record creation:
- Composes the full wallet record from crypto-derived fields (CC_DERIVE_WALLET_KEYS_V0) and payload fields
- Persists via registry with stable addressing
- Immutable binding once created
- Record structure matches V0 canonical schema

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_MUTABLE_JSON_V0 | CS | WRITE |
| 2 | CS_REGISTRY_V0 | CS | REGISTER |

---

## 4. Inputs

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| wallet_id | string | true | CC_GENERATE_WALLET_ID_V0 | Wallet identifier to register |
| actor_id | string | true | CC_RESOLVE_ACTOR_ID_V0 | Owner actor identifier |
| wallet_type | string | true | payload | Wallet type (e.g., business) |
| currency | string | true | payload | Currency code (e.g., BACHI) |
| network | string | true | payload | Network (e.g., testnet) |
| security_type | string | true | payload | Security type (e.g., hot) |
| eoa_public_key_hex | string | true | CC_DERIVE_WALLET_KEYS_V0 | EOA uncompressed public key, hex |
| eoa_address | string | true | CC_DERIVE_WALLET_KEYS_V0 | EOA Ethereum address, 0x-prefixed |
| eoa_derivation_path | string | true | CC_DERIVE_WALLET_KEYS_V0 | Full EOA BIP32 path |
| utxo_public_key_hex | string | true | CC_DERIVE_WALLET_KEYS_V0 | UTXO uncompressed public key, hex |
| utxo_address | string | true | CC_DERIVE_WALLET_KEYS_V0 | UTXO Ethereum address, 0x-prefixed |
| utxo_derivation_path | string | true | CC_DERIVE_WALLET_KEYS_V0 | Full UTXO BIP32 path |
| master_fingerprint | string | true | CC_DERIVE_WALLET_KEYS_V0 | HASH160(master_pubkey)[:4], hex |
| email_registration | string | true | payload | KYC registration email |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| result_status | string | Operation result |
| address | string | Registry address assigned |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Wallet registered successfully |
| ALREADY_EXISTS | Wallet already exists |
| VIOLATION | Invalid input format |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- Duplicate wallet results in ALREADY_EXISTS
- Invalid inputs result in VIOLATION
- Storage failure results in BACKEND_ERROR

---

## Machine

```yaml
cc_code: CC_CREATE_WALLET_RECORD_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Assemble and persist V0 wallet record

  inputs:
    wallet_id:
      type: string
      required: true
    actor_id:
      type: string
      required: true
    wallet_type:
      type: string
      required: true
    currency:
      type: string
      required: true
    network:
      type: string
      required: true
    security_type:
      type: string
      required: true
    eoa_public_key_hex:
      type: string
      required: true
    eoa_address:
      type: string
      required: true
    eoa_derivation_path:
      type: string
      required: true
    utxo_public_key_hex:
      type: string
      required: true
    utxo_address:
      type: string
      required: true
    utxo_derivation_path:
      type: string
      required: true
    master_fingerprint:
      type: string
      required: true
    email_registration:
      type: string
      required: true

  outputs:
    result_status:
      type: string
    address:
      type: string

  result_status_contract:
    allowed: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: write_wallet_state
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: WALLET
      op: WRITE
      inputs:
        key: $.inputs.wallet_id
        value:
          wallet_id: $.inputs.wallet_id
          actor_id: $.inputs.actor_id
          wallet_type: $.inputs.wallet_type
          account_model: hybrid
          status: active
          network: $.inputs.network
          currency: $.inputs.currency
          network_config:
            chain_id: 66
            rpc_endpoint: "http://localhost:8545"
          security:
            security_type: $.inputs.security_type
            key_scheme: secp256k1
            derivation_standard: bip44
            coin_type: 66
            master_fingerprint: $.inputs.master_fingerprint
            signing:
              derivation_root: "m/44'/66'/0'"
              address_index_start: 0
          addresses:
            eoa:
              - address: $.inputs.eoa_address
                derivation_path: $.inputs.eoa_derivation_path
                format: hex
                public_key: $.inputs.eoa_public_key_hex
            utxo:
              - address: $.inputs.utxo_address
                derivation_path: $.inputs.utxo_derivation_path
                format: hex
                public_key: $.inputs.utxo_public_key_hex
          state:
            eoa:
              nonce: 0
              balance: 0
            utxo:
              utxo_count: 0
              balance: 0
          metadata: {}
      outputs:
        result_status: $.capability_result.result_status
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: continue
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: register_wallet_index
      side_effect: capability_side_effects::CS_REGISTRY_V0
      op: REGISTER
      inputs:
        key: $.inputs.wallet_id
        target_cs: capability_side_effects::CS_MUTABLE_JSON_V0
        target_ref: $.inputs.wallet_id
      outputs:
        result_status: $.capability_result.result_status
        address: $.capability_result.address
      result_surface: [SUCCESS, ALREADY_EXISTS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        ALREADY_EXISTS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```
