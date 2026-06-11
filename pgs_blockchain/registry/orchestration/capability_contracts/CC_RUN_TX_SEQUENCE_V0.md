# CC_RUN_TX_SEQUENCE_V0

## Header (Mandatory)

- **Artifact Code:** CC_RUN_TX_SEQUENCE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_WORKFLOW_LOOP_V0

---

## 1. Intent

Execute the ordered TX workload sequence. For each TX spec in `tx_sequence`, dispatch to the appropriate typed TX workflow (WF_MINT_V0, WF_TRANSFER_V0, WF_BURN_V0, etc.) based on `tx_type`. This CC absorbs the TX loop internally (Collatz pattern) — the governing WF (WF_RUN_TX_WORKLOAD_V0) DAG is linear.

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration must be absorbed inside a CC (Collatz pattern). This CC is the loop container for the finite TX workload run. Each TX spec carries `tx_type` and all required payload fields for the targeted TX workflow — no payload construction occurs inside this CC. Dispatch mapping is declared explicitly in the `item_wf.wf_dispatch` spec.

Termination: the TX loop exits when `tx_sequence` is exhausted. Finite termination is guaranteed by the non-empty finite array declared in IN_TX_WORKLOAD_STARTED_V0.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_WORKFLOW_LOOP_V0 | CS | EXECUTE_SEQUENCE — iterate tx_sequence; dispatch by tx_type to typed TX WF |

**TX type dispatch mapping:**
- `TRANSFER` → `blockchain::WF_TRANSFER_V0`
- `STAKE` → `blockchain::WF_STAKE_V0`
- `UNSTAKE` → `blockchain::WF_UNSTAKE_V0`
- `MINT` → `blockchain::WF_MINT_V0`
- `BURN` → `blockchain::WF_BURN_V0`
- `POOL` → `blockchain::WF_POOL_V0`
- `REWARD` → `blockchain::WF_REWARD_V0`
- `SLASH` → `blockchain::WF_SLASH_V0`

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tx_sequence` | array | true | Non-empty ordered list of TX specs; each item carries `tx_type` and all required payload fields for the targeted TX workflow |
| `triggered_by` | string | true | Actor ID or system trigger reference |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| `result_status` | string | Operation result |
| `tx_submitted` | integer | Number of TX workflow invocations completed (`items_processed` from CS) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All TX specs processed; all typed TX WF invocations returned SUCCESS |
| VIOLATION | Any typed TX WF invocation returned non-SUCCESS, or unknown tx_type encountered; loop halted |
| BACKEND_ERROR | Loop executor or storage unavailable |

---

## 7. Failure Semantics

- VIOLATION from any typed TX WF invocation propagates as CC VIOLATION — the TX run halts; remaining TX specs do not execute
- Unknown `tx_type` value (not in dispatch mapping) propagates as VIOLATION
- BACKEND_ERROR propagates as a hard failure
- No partial commit — VIOLATION exits before remaining TX specs execute

---

## Machine

```yaml
cc_code: CC_RUN_TX_SEQUENCE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Collatz-pattern TX loop — dispatch tx_sequence by tx_type via CS_WORKFLOW_LOOP_V0

  inputs:
    tx_sequence:
      type: array
      required: true
      description: Non-empty ordered list of TX specs; each item carries tx_type and all payload fields for the targeted TX WF
    triggered_by:
      type: string
      required: true
      description: Actor ID or system trigger reference

  outputs:
    result_status:
      type: string
    tx_submitted:
      type: integer

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: execute_tx_sequence
      side_effect: capability_side_effects::CS_WORKFLOW_LOOP_V0
      op: EXECUTE_SEQUENCE
      inputs:
        sequence: $.inputs.tx_sequence
        triggered_by: $.inputs.triggered_by
        item_wf:
          wf_dispatch:
            key_field: tx_type
            mapping:
              TRANSFER: blockchain::WF_TRANSFER_V0
              STAKE: blockchain::WF_STAKE_V0
              UNSTAKE: blockchain::WF_UNSTAKE_V0
              MINT: blockchain::WF_MINT_V0
              BURN: blockchain::WF_BURN_V0
              POOL: blockchain::WF_POOL_V0
              REWARD: blockchain::WF_REWARD_V0
              SLASH: blockchain::WF_SLASH_V0
      outputs:
        tx_submitted: $.capability_result.items_processed
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: orchestration
  notes:
    - Collatz pattern — loop absorbed inside this CC; WF_RUN_TX_WORKLOAD_V0 DAG is linear
    - CS_WORKFLOW_LOOP_V0 EXECUTE_SEQUENCE governs dispatch — zero domain knowledge in substrate
    - tx_sequence items are TX spec objects; each carries tx_type and all payload fields for the targeted WF
    - Dispatch mapping declared here — this CC is the single authoritative mapping for tx_type → WF
    - VIOLATION from any TX WF invocation halts the loop — no partial execution
    - Unknown tx_type propagates as VIOLATION from the dispatcher
    - Termination guaranteed by finite tx_sequence declared in IN_TX_WORKLOAD_STARTED_V0
```
