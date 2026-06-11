"""
CT_PURE_SELECT_PROPOSER_V0

Pure Capability Transform (Atom)

Purpose:
    Select the block proposer for a given consensus round from the set of
    eligible validators using deterministic round-robin (modulo) selection.

Implementation:
    - Validates eligible_validators is non-empty
    - Validates round_number is non-negative
    - Returns eligible_validators[round_number % len(eligible_validators)].actor_id
"""

from typing import Dict, Any


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    if "eligible_validators" not in inputs:
        raise ValueError(
            "CT_PURE_SELECT_PROPOSER_V0: missing required input 'eligible_validators'"
        )
    if "round_number" not in inputs:
        raise ValueError(
            "CT_PURE_SELECT_PROPOSER_V0: missing required input 'round_number'"
        )

    eligible_validators = inputs["eligible_validators"]
    round_number = inputs["round_number"]

    if not isinstance(eligible_validators, list) or len(eligible_validators) == 0:
        raise ValueError(
            "CT_PURE_SELECT_PROPOSER_V0: VIOLATION — eligible_validators must be a non-empty array"
        )

    if not isinstance(round_number, int) or round_number < 0:
        raise ValueError(
            "CT_PURE_SELECT_PROPOSER_V0: VIOLATION — round_number must be a non-negative integer"
        )

    selected = eligible_validators[round_number % len(eligible_validators)]

    if "actor_id" not in selected:
        raise ValueError(
            "CT_PURE_SELECT_PROPOSER_V0: VIOLATION — validator record missing required field 'actor_id'"
        )

    return {"proposer_id": selected["actor_id"]}
