"""
CT_PURE_INCREMENT_WALLET_NONCE_V0

Pure Capability Transform (Atom)

Purpose:
    Create a copy of a wallet record with the EOA nonce incremented by 1.

Implementation:
    - Deep copies the wallet record
    - Increments state.eoa.nonce
    - Returns the updated record and the reserved (pre-increment) nonce
"""

import copy
from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "wallet_record" not in inputs:
        raise ValueError(
            "CT_PURE_INCREMENT_WALLET_NONCE_V0: missing required input 'wallet_record'"
        )

    wallet_record = inputs["wallet_record"]

    if not isinstance(wallet_record, dict):
        raise TypeError(
            f"CT_PURE_INCREMENT_WALLET_NONCE_V0: wallet_record must be object, got {type(wallet_record).__name__}"
        )

    # Deep copy to avoid mutating the original
    updated_record = copy.deepcopy(wallet_record)

    # Extract and increment nonce
    state = updated_record.get("state", {})
    eoa_state = state.get("eoa", {})
    current_nonce = eoa_state.get("nonce", 0)
    reserved_nonce = current_nonce

    eoa_state["nonce"] = current_nonce + 1
    state["eoa"] = eoa_state
    updated_record["state"] = state

    return {
        "updated_wallet_record": updated_record,
        "nonce": reserved_nonce
    }
