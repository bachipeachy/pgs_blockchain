"""
CT_PURE_DERIVE_BALANCES_V0

Pure Capability Transform (Atom)

Purpose:
    Derive wallet balances from the committed transaction history — a pure fold over every
    transaction in every committed block: debit the source wallet, credit the destination.

Inputs:
    committed_history — object; the append-only chain log (GET_ALL entries, each `{..., record: <block>}`)

Outputs:
    reconciled_balances — object; {wallet_id: balance} over all committed transactions
"""

from typing import Any, Dict


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "committed_history" not in inputs:
        raise ValueError("CT_PURE_DERIVE_BALANCES_V0: requires input 'committed_history'")
    balances: Dict[str, float] = {}
    for entry in inputs["committed_history"] or []:
        block = (entry or {}).get("record") or {}
        for tx in block.get("transactions", []) or []:
            amount = tx.get("amount", 0) or 0
            source = tx.get("from_wallet")
            destination = tx.get("to_wallet")
            if source is not None:
                balances[source] = balances.get(source, 0) - amount
            if destination is not None:
                balances[destination] = balances.get(destination, 0) + amount
    return {"reconciled_balances": balances}