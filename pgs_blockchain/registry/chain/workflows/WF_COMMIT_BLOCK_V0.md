# WF_COMMIT_BLOCK_V0

## Header (Mandatory)

- **Artifact Code:** WF_COMMIT_BLOCK_V0
- **Artifact Kind:** workflow
- **Governed By:** CONSTITUTION_WORKFLOW_V0
- **Version:** v0
- **Status:** draft
- **Supersedes:** NONE
- **Dependencies:** blockchain::IN_COMMIT_BLOCK_V0, blockchain::CC_VALIDATE_PREDECESSOR_LINK_V0, blockchain::CC_COMMIT_BLOCK_CANONICAL_V0, blockchain::CC_RECONCILE_BALANCES_V0

---

## 1. Intent

Commit a proposed block to the canonical chain

---

## 2. Rationale



---

## 3. Execution Graph

```
start: IN_COMMIT_BLOCK_V0

IN_COMMIT_BLOCK_V0 [IN] ACK → CC_VALIDATE_PREDECESSOR_LINK_V0, NACK → EXIT
CC_VALIDATE_PREDECESSOR_LINK_V0 [CC] SUCCESS → CC_COMMIT_BLOCK_CANONICAL_V0, VIOLATION → EXIT
CC_COMMIT_BLOCK_CANONICAL_V0 [CC] SUCCESS → CC_RECONCILE_BALANCES_V0
CC_RECONCILE_BALANCES_V0 [CC] SUCCESS → EXIT_SUCCESS
EXIT_SUCCESS [EXIT] reason=COMPLETED
EXIT [EXIT] reason=EXITED
```

---

## 4. Nodes

| Node | Type | Code/Reason |
|---|---|---|
| IN_COMMIT_BLOCK_V0 | IN | blockchain::IN_COMMIT_BLOCK_V0 |
| CC_VALIDATE_PREDECESSOR_LINK_V0 | CC | blockchain::CC_VALIDATE_PREDECESSOR_LINK_V0 |
| CC_COMMIT_BLOCK_CANONICAL_V0 | CC | blockchain::CC_COMMIT_BLOCK_CANONICAL_V0 |
| CC_RECONCILE_BALANCES_V0 | CC | blockchain::CC_RECONCILE_BALANCES_V0 |
| EXIT_SUCCESS | EXIT | COMPLETED |
| EXIT | EXIT | EXITED |

---

## 5. Admission

- **Requires:** NONE
- **Forbids:** NONE

---

## Machine

```yaml
wf_code: WF_COMMIT_BLOCK_V0
version: v0
governed_by: fb.topology::CONSTITUTION_WORKFLOW_V0
runtime_binding: blockchain::RB_COMMIT_BLOCK_V0
core:
  runtime_binding: blockchain::RB_COMMIT_BLOCK_V0
  summary: Commit a proposed block to the canonical chain
  admission:
    requires: []
    forbids: []
  start_node: IN_COMMIT_BLOCK_V0
  nodes:
    IN_COMMIT_BLOCK_V0:
      type: IN
      code: blockchain::IN_COMMIT_BLOCK_V0
      next:
        ACK: CC_VALIDATE_PREDECESSOR_LINK_V0
        NACK: EXIT
    CC_VALIDATE_PREDECESSOR_LINK_V0:
      type: CC
      code: blockchain::CC_VALIDATE_PREDECESSOR_LINK_V0
      inputs:
        proposed_block: $.payload.proposed_block
      next:
        SUCCESS: CC_COMMIT_BLOCK_CANONICAL_V0
        VIOLATION: EXIT
    CC_COMMIT_BLOCK_CANONICAL_V0:
      type: CC
      code: blockchain::CC_COMMIT_BLOCK_CANONICAL_V0
      inputs:
        proposed_block: $.payload.proposed_block
      next:
        SUCCESS: CC_RECONCILE_BALANCES_V0
    CC_RECONCILE_BALANCES_V0:
      type: CC
      code: blockchain::CC_RECONCILE_BALANCES_V0
      next:
        SUCCESS: EXIT_SUCCESS
    EXIT_SUCCESS:
      type: EXIT
      reason: COMPLETED
    EXIT:
      type: EXIT
      reason: EXITED
```
