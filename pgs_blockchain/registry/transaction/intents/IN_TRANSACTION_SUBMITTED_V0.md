# IN_TRANSACTION_SUBMITTED_V0

## Header (Mandatory)

- **Artifact Code:** IN_TRANSACTION_SUBMITTED_V0
- **Artifact Kind:** intent
- **Governed By:** CONSTITUTION_INTENT_V0
- **Version:** v0
- **Status:** RETIRED
- **Supersedes:** NONE
- **Dependencies:** WF_SUBMIT_TRANSACTION_V0

---

## 1. Intent

Submit an ETH transaction from a wallet, validating, signing, and persisting to the local mempool.

---

## 2. Rationale

Transaction submission requires:
- Actor must be resolved (verified)
- Transaction structure and policy must be validated
- Nonce must be atomically reserved
- Transaction must be signed with the user-supplied mnemonic
- Signed transaction is persisted to append-only mempool

---

## 3. Workflow Binding

| Target | Description |
|--------|-------------|
| WF_SUBMIT_TRANSACTION_V0 | Workflow that processes this intent |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actor_record | object | true | Actor record for resolution |
| wallet_id | string | true | Source wallet identifier |
| to_address | string | true | Destination address (0x-prefixed) |
| value | string | true | Transfer value in wei |
| gas_limit | integer | false | Gas limit (default 21000) |
| max_fee_per_gas | string | false | Max fee per gas in wei (default "20000000000") |
| max_priority_fee_per_gas | string | false | Max priority fee in wei (default "1000000000") |
| data | string | false | Transaction data (default "0x") |
| mnemonic | string | true | BIP-39 mnemonic for key re-derivation (transient secret) |

---

## 5. Outcomes

| Outcome | Description |
|---------|-------------|
| ACK | Transaction submission initiated |
| NACK | Transaction submission rejected |

---

## 6. Domain

- **Domain:** pgs.finance.transaction

---

## Machine

```yaml
in_code: IN_TRANSACTION_SUBMITTED_V0
version: v0
status: RETIRED
superseded_by: [IN_TRANSFER_V0, IN_STAKE_V0, IN_UNSTAKE_V0, IN_MINT_V0, IN_BURN_V0, IN_POOL_V0, IN_REWARD_V0, IN_SLASH_V0]
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: Submit ETH transaction from wallet
  workflow: WF_SUBMIT_TRANSACTION_V0

  inputs:
    actor_record:
      type: object
      required: true
      description: Actor record for resolution
    wallet_id:
      type: string
      required: true
      description: Source wallet identifier
    to_address:
      type: string
      required: true
      description: Destination address (0x-prefixed hex)
    value:
      type: string
      required: true
      description: Transfer value in wei
    gas_limit:
      type: integer
      default: 21000
      description: Gas limit
    max_fee_per_gas:
      type: string
      default: "20000000000"
      description: Max fee per gas in wei
    max_priority_fee_per_gas:
      type: string
      default: "1000000000"
      description: Max priority fee per gas in wei
    data:
      type: string
      default: "0x"
      description: Transaction data hex
    mnemonic:
      type: string
      required: true
      description: BIP-39 mnemonic for key re-derivation (transient secret)

  outcomes:
    ACK:
      description: Transaction submission initiated
    NACK:
      description: Transaction submission rejected

  admission:
    requires:
      - EV_WALLET_CREATED_V0

extensions:
  domain: pgs.finance.transaction
```
