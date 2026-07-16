"""
CT_PURE_EXTRACT_PREDECESSOR_HASH_V0

Pure Capability Transform (Atom)

Purpose:
    Extract the predecessor hash carried by a proposed block — the content hash of the
    block this one chains onto.

Inputs:
    block — object; carries a `predecessor_hash` field

Outputs:
    predecessor_hash — string; the block's declared predecessor content hash
"""

from typing import Any, Dict


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "block" not in inputs:
        raise ValueError("CT_PURE_EXTRACT_PREDECESSOR_HASH_V0: requires input 'block'")
    block = inputs["block"] or {}
    return {"predecessor_hash": block.get("predecessor_hash")}