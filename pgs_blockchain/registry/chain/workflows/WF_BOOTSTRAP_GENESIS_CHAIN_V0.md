# WF_BOOTSTRAP_GENESIS_CHAIN_V0

## Header (Mandatory)

- **Artifact Code:** WF_BOOTSTRAP_GENESIS_CHAIN_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** blockchain::IN_BOOTSTRAP_GENESIS_CHAIN_V0, blockchain::CC_CREATE_GENESIS_BLOCK_V0

---

## 1. Intent

Bootstrap the genesis chain and initialise the supply

---

## 2. Rationale



---

## 3. Execution Graph

```
start: IN_BOOTSTRAP_GENESIS_CHAIN_V0

IN_BOOTSTRAP_GENESIS_CHAIN_V0 [IN] ACK → CC_CREATE_GENESIS_BLOCK_V0, NACK → EXIT
CC_CREATE_GENESIS_BLOCK_V0 [CC] SUCCESS → EXIT_SUCCESS
EXIT_SUCCESS [EXIT] reason=COMPLETED
EXIT [EXIT] reason=EXITED
```

---

## 4. Nodes

| Node | Type | Code/Reason |
|---|---|---|
| IN_BOOTSTRAP_GENESIS_CHAIN_V0 | IN | blockchain::IN_BOOTSTRAP_GENESIS_CHAIN_V0 |
| CC_CREATE_GENESIS_BLOCK_V0 | CC | blockchain::CC_CREATE_GENESIS_BLOCK_V0 |
| EXIT_SUCCESS | EXIT | COMPLETED |
| EXIT | EXIT | EXITED |

---

## 5. Admission

- **Requires:** NONE
- **Forbids:** NONE

---

## Machine

```yaml
wf_code: WF_BOOTSTRAP_GENESIS_CHAIN_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_BOOTSTRAP_GENESIS_CHAIN_V0
core:
  runtime_binding: blockchain::RB_BOOTSTRAP_GENESIS_CHAIN_V0
  summary: Bootstrap the genesis chain and initialise the supply
  admission:
    requires: []
    forbids: []
  start_node: IN_BOOTSTRAP_GENESIS_CHAIN_V0
  nodes:
    IN_BOOTSTRAP_GENESIS_CHAIN_V0:
      type: IN
      code: blockchain::IN_BOOTSTRAP_GENESIS_CHAIN_V0
      next:
        ACK: CC_CREATE_GENESIS_BLOCK_V0
        NACK: EXIT
    CC_CREATE_GENESIS_BLOCK_V0:
      type: CC
      code: blockchain::CC_CREATE_GENESIS_BLOCK_V0
      inputs:
        genesis_block_content: $.payload.genesis_block_content
      next:
        SUCCESS: EXIT_SUCCESS
    EXIT_SUCCESS:
      type: EXIT
      reason: COMPLETED
    EXIT:
      type: EXIT
      reason: EXITED
```
