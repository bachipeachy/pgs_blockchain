# CC_FORM_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** CC_FORM_BLOCK_V0
- **Artifact Kind:** capability_contract
- **Governed By:** CONSTITUTION_CAPABILITY_CONTRACT_V0
- **Version:** v0
- **Status:** canonical
- **Supersedes:** NONE
- **Dependencies:** CT_PURE_GENERATE_ID_V0, CT_PURE_ASSEMBLE_RECORD_V0, CS_MUTABLE_JSON_V0, CS_APPENDONLY_JSONL_V0

---

## 1. Intent

Form a new block from the selected proposer, pending transactions, and round context. Write the block to the BLOCKS store and append a block lifecycle event to BLOCK_EVENTS.

---

## 2. Rationale

Block formation is the canonical write operation for the `blockchain::block` subdomain. All writes are scoped to block-owned stores (BLOCKS, BLOCK_EVENTS). No cross-subdomain writes occur in this CC. The block record is the primary unit of the block subdomain.

---

## 3. Pipeline

| Step | Capability | Type | Operation |
|------|------------|------|-----------|
| 1 | CT_PURE_GENERATE_ID_V0 | CT | Generate block_id (prefix: B) |
| 2 | CT_PURE_ASSEMBLE_RECORD_V0 | CT | Assemble block_record |
| 3 | CS_MUTABLE_JSON_V0 | CS | WRITE to BLOCKS store |
| 4 | CS_APPENDONLY_JSONL_V0 | CS | APPEND to BLOCK_EVENTS store |

---

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_id | integer | true | Consensus round number (maps to block height) |
| slot | integer | true | Slot number within the epoch |
| epoch | integer | true | Epoch number |
| proposer_id | string | true | actor_id of the proposing validator |
| tx_ids | array | true | Ordered list of transaction IDs to include |
| timestamp | string | true | ISO 8601 block formation timestamp |

---

## 5. Outputs

| Field | Type | Description |
|-------|------|-------------|
| block_id | string | Generated block identifier (B-prefixed) |

---

## 6. Result Status Contract

| Status | Condition |
|--------|-----------|
| SUCCESS | Block formed, written, and event appended |
| VIOLATION | Invalid input |
| BACKEND_ERROR | Storage unavailable |

---

## 7. Failure Semantics

- VIOLATION on missing or invalid required inputs
- BACKEND_ERROR propagates as a hard failure from any CS step
- block_id is returned on SUCCESS only

---

## Machine

```yaml
cc_code: CC_FORM_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  summary: Form a block, write to BLOCKS store, append to BLOCK_EVENTS

  inputs:
    round_id:
      type: integer
      required: true
      description: Consensus round number (maps to block height)
    slot:
      type: integer
      required: true
      description: Slot number within the epoch
    epoch:
      type: integer
      required: true
      description: Epoch number
    proposer_id:
      type: string
      required: true
    tx_ids:
      type: array
      required: true
      items:
        type: string
    timestamp:
      type: string
      required: true
      format: date-time

  outputs:
    block_id:
      type: string

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]
    on_input_failure: VIOLATION

  pipeline:
    - step: generate_block_id
      transform: capability_transforms::CT_PURE_GENERATE_ID_V0
      inputs:
        prefix: B
        data: $.inputs.round_id
      outputs:
        block_id: $.capability_result.id
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: assemble_block_record
        VIOLATION: exit

    - step: assemble_block_record
      transform: capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0
      inputs:
        fields:
          block_id: $.results.generate_block_id.block_id
          round_id: $.inputs.round_id
          slot: $.inputs.slot
          epoch: $.inputs.epoch
          proposer_id: $.inputs.proposer_id
          tx_ids: $.inputs.tx_ids
          is_canonical: false
          status: PROPOSED
          timestamp: $.inputs.timestamp
      outputs:
        block_record: $.capability_result.record
      result_surface: [SUCCESS, VIOLATION]
      on_result:
        SUCCESS: write_block
        VIOLATION: exit

    - step: write_block
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
      store: BLOCKS
      op: WRITE
      inputs:
        key: $.results.generate_block_id.block_id
        value: $.results.assemble_block_record.block_record
      outputs: {}
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: append_block_event
        VIOLATION: exit
        BACKEND_ERROR: exit

    - step: append_block_event
      side_effect: capability_side_effects::CS_APPENDONLY_JSONL_V0
      store: BLOCK_EVENTS
      op: APPEND
      inputs:
        stream_id: $.results.generate_block_id.block_id
        record:
          event_code: EV_BLOCK_PROPOSED_V0
          block_id: $.results.generate_block_id.block_id
          round_id: $.inputs.round_id
          slot: $.inputs.slot
          epoch: $.inputs.epoch
          proposer_id: $.inputs.proposer_id
          tx_ids: $.inputs.tx_ids
          timestamp: $.inputs.timestamp
      outputs:
        block_id: $.results.generate_block_id.block_id
      result_surface: [SUCCESS, VIOLATION, BACKEND_ERROR]
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit

extensions:
  subdomain: block
  notes:
    - All writes scoped to blockchain::block stores (BLOCKS, BLOCK_EVENTS)
    - block_id propagated to caller for CC_RECORD_CONSENSUS_ROUND_V0
```
