"""
CT_PURE_DERIVE_SLOT_EPOCH_V0

Pure Capability Transform (Atom)

Purpose:
    Derive slot context fields from a globally-increasing slot number and
    slot start timestamp. Used by CC_PREPARE_SLOT_CONTEXT_V0 to map raw
    slot clock state into the richer context needed for block proposal and
    slot execution routing.

Outputs:
    round_number  — pass-through of slot_number; satisfies WF_PROPOSE_BLOCK_V0 contract
    slot_index    — intra-epoch position (0-based); slot_number % slots_per_epoch
    epoch_number  — monotonically increasing epoch counter; slot_number // slots_per_epoch
    timestamp     — pass-through of slot_start_ts

Field naming precision:
    slot_number  — globally-increasing counter; never resets
    slot_index   — intra-epoch position; resets to 0 at each epoch boundary
    These are semantically distinct; use exact field names throughout.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

_BASE_SLOT_TS = datetime(2026, 1, 1, tzinfo=timezone.utc)
_SLOT_DURATION_SECONDS = 30


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    slot_number = inputs.get("slot_number")
    slot_start_ts = inputs.get("slot_start_ts")
    slots_per_epoch = inputs.get("slots_per_epoch") or 32

    if slot_number is None:
        raise ValueError("CT_PURE_DERIVE_SLOT_EPOCH_V0: missing required input 'slot_number'")
    if not isinstance(slot_number, int) or slot_number < 0:
        raise ValueError(
            f"CT_PURE_DERIVE_SLOT_EPOCH_V0: slot_number must be a non-negative integer, got {slot_number!r}"
        )
    if not isinstance(slots_per_epoch, int) or slots_per_epoch < 1:
        raise ValueError(
            f"CT_PURE_DERIVE_SLOT_EPOCH_V0: slots_per_epoch must be a positive integer, got {slots_per_epoch!r}"
        )

    if slot_start_ts is None:
        slot_start_ts = (
            _BASE_SLOT_TS + timedelta(seconds=slot_number * _SLOT_DURATION_SECONDS)
        ).isoformat().replace("+00:00", "Z")

    return {
        "round_number": slot_number,
        "slot_index": slot_number % slots_per_epoch,
        "epoch_number": slot_number // slots_per_epoch,
        "timestamp": slot_start_ts,
    }
