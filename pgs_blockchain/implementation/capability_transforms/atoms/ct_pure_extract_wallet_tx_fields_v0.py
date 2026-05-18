"""
CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0

Pure Capability Transform (Atom)

Purpose:
    Extract transaction-relevant fields from a wallet record.
    Handles array indexing and nested path extraction that the
    expression resolver cannot perform.

Implementation:
    - Extracts from_address from addresses.eoa[0].address
    - Extracts current nonce from state.eoa.nonce
    - Pure function, no side effects
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "wallet_record" not in inputs:
        raise ValueError(
            "CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0: missing required input 'wallet_record'"
        )

    wallet_record = inputs["wallet_record"]

    if not isinstance(wallet_record, dict):
        raise TypeError(
            f"CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0: wallet_record must be object, got {type(wallet_record).__name__}"
        )

    # Extract EOA address
    # We return None if not found, allowing the Capability Contract to handle policy violations
    addresses = wallet_record.get("addresses", {})
    eoa_list = addresses.get("eoa", [])

    from_address = None
    if eoa_list and isinstance(eoa_list, list) and len(eoa_list) > 0:
        from_address = eoa_list[0].get("address")

    # Extract current nonce
    state = wallet_record.get("state", {})
    eoa_state = state.get("eoa", {})
    current_nonce = eoa_state.get("nonce", 0)

    # Extract actor_id for validation
    actor_id = wallet_record.get("actor_id")

    # CONSTITUTIONAL: Atoms return flat data.
    # The execution layer (execute_ct.py) handles mapping to the contract envelope.
    return {
        "from_address": from_address,
        "current_nonce": current_nonce,
        "actor_id": actor_id
    }
