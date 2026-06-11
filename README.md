# pgs_blockchain

**A protocol-defined blockchain domain built on Protocol-Governed Systems.**

This repository demonstrates how a complete system — identity, wallets, transactions — can be expressed as declarative protocol artifacts and executed without embedding business logic in code.
It is not a simulation or mock implementation.
It implements faithfully family of Bitcoin Improvement plans -- BIP specifications.
It implements Etherium standards wherever applicable e.g., HDWallet.
The crypto library is fully aligned to BIP and ETH crypto currency.
It is a working domain built entirely through protocol.
It is obvious blockchain implementation is partial upto transaction submission only.

Behavior is declared in protocol, executed by runtime, implemented in capabilities, and observed via traces and state.

> **New to PGS?** This is one of the repositories in the Protocol-Governed Systems ecosystem.
> For orientation, architecture overview, and end-to-end execution, start at [pgs_workspace](https://github.com/bachipeachy/pgs_workspace).

---

## Execution model

Every workflow execution follows this path:

```
IN_ → WF_ → CC_ → (CT_ / CS_) → Trace
```

| Concern | What it does |
|---------|-------------|
| `IN_` Intent | Admission gate — validates payload before anything runs |
| `WF_` Workflow | Execution graph — declares which CCs run and in what order |
| `CC_` Capability Contract | Named DAG node — declares inputs, outputs, and routing outcomes |
| `CT_` Capability Transform | Pure computation — deterministic, no side effects |
| `CS_` Capability Side Effect | Controlled state change — registry write, event append |
| `RB_` Runtime Binding | Maps declared capabilities to implementations at build time |
| Trace | Append-only execution record — ground truth of what happened |

The runtime traverses this graph exactly as declared. It has no domain knowledge. All behavior lives in the compiled snapshot.

---

## Build lifecycle

```
compile → build → run
```

| Phase | What happens | Where |
|-------|-------------|-------|
| **compile** | Source artifacts validated against invariants | `pgs_governance` / `pgs_compiler` |
| **build** | Validated artifacts materialized into a closed snapshot | `pgs_compiler` → `pgs_workspace/protocol_snapshot/` |
| **run** | Runtime reads snapshot and executes | `pgs_workspace` (pgs_runtime CLI) |

The snapshot is sealed at build time. No behavior enters at execution time that was not in the snapshot.

---

## What this repository contains

Blockchain behavior is expressed across four concern areas:

| Concern | What it covers |
|---------|---------------|
| **Identity** | Actor registration and verification |
| **Wallet** | Keypair generation and state management |
| **Transaction** | Submission and validation |
| **Consensus** | Extensible surface (see below) |

Each concern is implemented as protocol artifacts — workflows, capability contracts, transforms, and side-effects. No logic is embedded in the runtime.

---

## Workflows

```
blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0
blockchain::WF_VERIFY_ACTOR_V0
blockchain::WF_CREATE_WALLET_V0
blockchain::WF_SUBMIT_TRANSACTION_V0
```

These workflows execute through the generic runtime and produce:
- deterministic traces
- governed side-effects
- append-only event history

Test payloads for each workflow live in `pgs_blockchain/testbed/` under their respective concern directories.

---

## Running these workflows

From `pgs_workspace`:

```bash
pgs_runtime run \
  --wf blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0 \
  --payload ../pgs_blockchain/pgs_blockchain/testbed/identity/payload_register_actor.json \
  --data-root $(pwd)/data \
  --workspace .
```

The runtime knows nothing about blockchain. All domain semantics are expressed in protocol artifacts. It traverses the precompiled DAG.

---

## State model

The domain demonstrates two complementary storage patterns:

| Structure | Semantics | Purpose |
|-----------|-----------|---------|
| `data/registry/` | Idempotent | Constrained state — uniqueness enforced |
| `data/events/` | Append-only | Complete history — every attempt recorded |

This separation is structural, not convention. Running the same workflow twice:
- Registry detects the duplicate → returns `ALREADY_EXISTS`
- Event stream still records the attempt → always appends

State is constrained. History remains complete.

---

## Outcome-driven behavior

Side-effects return explicit outcomes:

```
SUCCESS
ALREADY_EXISTS
VIOLATION
```

Workflows route based on these outcomes. There is no implicit error handling or hidden branching. Every execution path is a named edge in the compiled DAG.

---

## Extending the blockchain surface

This domain is intentionally structured to grow. You do not modify existing workflows. You add new artifacts.

### Add new capability transforms (CT)

```
CT_VALIDATE_TRANSACTION_SIGNATURE_V0
CT_BUILD_BLOCK_V0
CT_SELECT_VALIDATOR_V0
CT_CALCULATE_GAS_V0
CT_EXECUTE_CONTRACT_V0
```

### Add new side-effects (CS)

```
CS_APPEND_MEMPOOL_ENTRY_V0
CS_REMOVE_MEMPOOL_ENTRY_V0
CS_APPEND_BLOCKCHAIN_V0
CS_COMMIT_BLOCK_V0
CS_PERSIST_CONTRACT_STATE_V0
```

### Add new workflows (WF)

```
WF_PROCESS_MEMPOOL_V0
WF_PROPOSE_BLOCK_V0
WF_VALIDATE_BLOCK_V0
WF_FINALIZE_BLOCK_V0
```

### Add new storage semantics

- Append-only chain log (block history)
- Snapshot state (account balances)
- Hybrid models (UTXO vs account-based)

All controlled via CS declarations — no runtime changes required.

---

## What you do NOT change to extend

To add new blockchain capabilities, you do not modify:
- `pgs_runtime` — the execution engine stays unchanged
- existing workflows — new behavior is additive
- any cross-domain infrastructure

You extend by authoring new protocol artifacts. That is the entire extension mechanism.

---

## Repo structure

```
pgs_blockchain/
└── pgs_blockchain/
    ├── testbed/
    │   ├── identity/    ← payloads for actor workflows
    │   ├── wallet/      ← payloads for wallet workflows
    │   ├── transaction/ ← payloads for transaction workflows
    │   └── static/      ← browser UI client
    └── ...
```

---

## Where this fits in the system

| Repo | Role |
|------|------|
| `pgs_governance` + `pgs_compiler` | Define and compile protocol artifacts |
| `pgs_runtime` | Executes compiled workflows |
| `pgs_capabilities` | Implements CT/CS used here |
| **`pgs_blockchain` ← here** | **Defines domain behavior** |
| `pgs_ai_governance` | Governance domain |
| `pgs_change_mgmt` | Governed SDLC — Change Request to Authoring Mandate (new in v0.5.0) |
| `pgs_workspace` | Entry point — run and observe |

---

## Research context

> *"Extensibility by declaration, not refactor."*

At domain scale.

Adding new blockchain capabilities requires new protocol artifacts. The runtime, library, and existing workflows remain unchanged. The cost of adding a mempool, a block proposal mechanism, or a fee model is bounded by the artifacts for that capability — nothing else changes.

---

## Core idea

This is not a blockchain implementation.  
It is a blockchain defined as a protocol.

---

## Final note

If extending this domain requires modifying the runtime, the design has been violated.  
Add artifacts. The system already knows how to execute them.
---

## License

Apache-2.0. See LICENSE and NOTICE for details.
