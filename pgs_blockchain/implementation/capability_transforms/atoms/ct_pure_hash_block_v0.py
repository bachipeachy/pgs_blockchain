"""
CT_PURE_HASH_BLOCK_V0

Pure Capability Transform (Atom)

Purpose:
    Compute a block's content signature by canonically hashing the block.
    Canonical serialization (sorted keys, no whitespace) → Keccak-256 → 0x-prefixed hex.

Inputs:
    block — object; the block to hash

Outputs:
    content_hash — string; 0x-prefixed Keccak-256 of the canonical block bytes
"""

import json
from typing import Any, Dict

from Crypto.Hash import keccak


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "block" not in inputs:
        raise ValueError("CT_PURE_HASH_BLOCK_V0: requires input 'block'")
    canonical = json.dumps(inputs["block"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    k = keccak.new(digest_bits=256)
    k.update(canonical)
    return {"content_hash": "0x" + k.hexdigest()}