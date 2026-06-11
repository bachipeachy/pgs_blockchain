# CC_EXECUTE_SLOT_SEQUENCE_V0

## Header (Mandatory)

- **Artifact Code:** CC_EXECUTE_SLOT_SEQUENCE_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** CS_WORKFLOW_LOOP_V0

---

## 1. Intent

Execute a finite ordered sequence of consensus slots. For each slot descriptor in `slot_schedule`, submit each declared transaction to its typed transaction workflow, then invoke WF_PROPOSE_BLOCK_V0 for that slot. This CC absorbs the slot loop internally (Collatz pattern) — the governing WF (WF_RUN_CONSENSUS_SLOTS_V0) DAG is linear.

---

## 2. Rationale

PGS WF DAGs have no loop construct — all iteration must be absorbed inside a CC (Collatz pattern). This CC is the loop container for the finite slot run. All domain behavior (transaction submission, block proposal, round recording) lives in the governed WFs invoked per slot. This CC contains no domain logic — it declares a fully parametric dispatch spec to CS_WORKFLOW_LOOP_V0, which iterates the sequence and invokes the governed WFs.

Cross-subdomain write rule: this CC does NOT write to any store directly. All writes (BLOCKS, CONSENSUS_ROUNDS, TRANSACTION) occur through the owned CCs of their respective subdomains, invoked via governed WFs. The Collatz pattern ensures that all side effects are mediated through governed capability contracts with full trace coverage.

Termination: the slot loop exits when `slot_schedule` is exhausted. There is no external kill signal and no polling. Finite termination is guaranteed by the non-empty finite array declared in IN_CONSENSUS_SLOTS_V0.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CS_WORKFLOW_LOOP_V0 | CS | EXECUTE_SEQUENCE — iterate slot_schedule with fully declarative dispatch spec |

**Dispatch spec declared in step inputs:**
- `item_sub_sequence`: for each slot, iterate `transactions` array; dispatch by `tx_type` key field → typed transaction WF (WF_TRANSFER_V0, WF_STAKE_V0, etc.)
- `item_wf`: invoke WF_PROPOSE_BLOCK_V0 with slot fields {round_number, slot, epoch, timestamp} + triggered_by inject

Sub-sequence (transactions) is processed BEFORE item WF (block proposal) — transactions must be in mempool before the block is proposed.

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| slot_schedule | array | true | Ordered list of slot descriptors from IN_CONSENSUS_SLOTS_V0 |
| triggered_by | string | true | System actor_id initiating the slot run |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| slots_executed | integer | Number of slot descriptors processed (items_processed from CS) |
| tx_submitted | integer | Total transaction WF invocations across all slots (sub_items_processed from CS) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | All slot descriptors processed; all governed WF invocations returned SUCCESS |
| VIOLATION | Any governed WF invocation returned non-SUCCESS; loop halted |
| BACKEND_ERROR | Storage or executor unavailable |

---

## 7. Failure Semantics

- VIOLATION from any governed WF invocation (transaction or block proposal) propagates as CC VIOLATION — the slot run halts
- BACKEND_ERROR propagates as a hard failure
- This CC never partially commits — VIOLATION exits before remaining slots execute

---

## Machine

```yaml
cc_code: CC_EXECUTE_SLOT_SEQUENCE_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Collatz-pattern slot loop — execute all slots via CS_WORKFLOW_LOOP_V0 declarative dispatch

  inputs:
    slot_schedule:
      type: array
      required: true
      description: Ordered list of slot descriptors; each contains transactions and block proposal fields
    triggered_by:
      type: string
      required: true
      description: System actor_id initiating the slot run

  outputs:
    slots_executed:
      type: integer
    tx_submitted:
      type: integer

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: execute_slot_sequence
      side_effect: capability_side_effects::CS_WORKFLOW_LOOP_V0
      op: EXECUTE_SEQUENCE
      inputs:
        sequence: $.inputs.slot_schedule
        triggered_by: $.inputs.triggered_by
        item_wf:
          code: blockchain::WF_PROPOSE_BLOCK_V0
          payload_fields:
            round_number: round_number
            slot: slot
            epoch: epoch
            timestamp: timestamp
          inject:
            triggered_by: $.inputs.triggered_by
        item_sub_sequence:
          field: transactions
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
        slots_executed: $.capability_result.items_processed
        tx_submitted: $.capability_result.sub_items_processed
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: consensus_pos
  notes:
    - Collatz pattern — loop absorbed inside this CC; WF_RUN_CONSENSUS_SLOTS_V0 DAG is linear (3 nodes)
    - CS_WORKFLOW_LOOP_V0 EXECUTE_SEQUENCE is the governed side effect — zero domain knowledge in substrate
    - All dispatch logic declared in item_wf and item_sub_sequence inputs — CC is the domain authority
    - Sub-sequence (transactions) processed BEFORE item_wf (block proposal) per slot
    - Typed WF dispatch: TRANSFER→WF_TRANSFER_V0, STAKE→WF_STAKE_V0, UNSTAKE→WF_UNSTAKE_V0, MINT→WF_MINT_V0, BURN→WF_BURN_V0, POOL→WF_POOL_V0, REWARD→WF_REWARD_V0, SLASH→WF_SLASH_V0
    - No direct writes to any store — all writes occur through owned CCs of their respective subdomains
    - Termination guaranteed by finite slot_schedule (non-empty array declared in IN_CONSENSUS_SLOTS_V0)
    - VIOLATION from any WF invocation halts the loop — no partial commit
    - $.inputs.triggered_by inside inject dict is resolved by dispatcher input resolution (recursive dict handling)
```
