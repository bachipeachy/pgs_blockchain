"""
CT_PURE_BUILD_ETH_TRANSACTION_V0

Pure Capability Transform (Atom)

Purpose:
    Build an unsigned EIP-1559 (Type 2) Ethereum transaction as RLP-encoded bytes.

Implementation:
    - Pure Python RLP encoding (no external dependency)
    - EIP-1559 format: 0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas,
      max_fee_per_gas, gas_limit, to, value, data, access_list])
    - Returns unsigned_tx_bytes as hex string
    - Pure, fail-fast implementation
"""

from typing import Dict, Any, List, Union


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    # 1. Assert required inputs exist and are not None
    if inputs is None:
        raise ValueError("CT_PURE_BUILD_ETH_TRANSACTION_V0: inputs must not be None")

    required = ["chain_id", "nonce", "to", "value"]
    for field in required:
        if field not in inputs:
            raise ValueError(
                f"CT_PURE_BUILD_ETH_TRANSACTION_V0: missing required input '{field}'"
            )
        if inputs[field] is None:
            raise ValueError(
                f"CT_PURE_BUILD_ETH_TRANSACTION_V0: input '{field}' must not be None"
            )

    try:
        chain_id = int(inputs["chain_id"])
        nonce = int(inputs["nonce"])
        
        # Default values for optional fields if they are missing OR None
        max_priority_fee_per_gas_raw = inputs.get("max_priority_fee_per_gas")
        max_priority_fee_per_gas = int(max_priority_fee_per_gas_raw if max_priority_fee_per_gas_raw is not None else "1000000000")
        
        max_fee_per_gas_raw = inputs.get("max_fee_per_gas")
        max_fee_per_gas = int(max_fee_per_gas_raw if max_fee_per_gas_raw is not None else "20000000000")
        
        gas_limit_raw = inputs.get("gas_limit")
        gas_limit = int(gas_limit_raw if gas_limit_raw is not None else 21000)
        
        to = inputs["to"]
        value = int(inputs["value"])
        
        data_raw = inputs.get("data")
        data = data_raw if data_raw is not None else "0x"
        
        access_list_raw = inputs.get("access_list")
        access_list = access_list_raw if access_list_raw is not None else []

        # 2. Pure computation (no filesystem/env dependency)
        
        # Encode 'to' address as bytes
        to_hex = to
        if to_hex.startswith("0x") or to_hex.startswith("0X"):
            to_hex = to_hex[2:]
        to_bytes = bytes.fromhex(to_hex)

        if len(to_bytes) != 20:
            raise ValueError(
                f"CT_PURE_BUILD_ETH_TRANSACTION_V0: 'to' address must be 20 bytes, got {len(to_bytes)}"
            )

        # Encode 'data' as bytes
        data_hex = data
        if data_hex.startswith("0x") or data_hex.startswith("0X"):
            data_hex = data_hex[2:]
        data_bytes = bytes.fromhex(data_hex) if data_hex else b""

        # Build EIP-1559 Type 2 transaction fields
        tx_fields = [
            chain_id,
            nonce,
            max_priority_fee_per_gas,
            max_fee_per_gas,
            gas_limit,
            to_bytes,
            value,
            data_bytes,
            access_list,
        ]

        # RLP encode the fields list
        rlp_encoded = _rlp_encode(tx_fields)

        # EIP-1559 Type 2 prefix: 0x02
        unsigned_tx = bytes([0x02]) + rlp_encoded
        unsigned_tx_hex = "0x" + unsigned_tx.hex()

        result = {
            "unsigned_tx_bytes": unsigned_tx_hex
        }

        # 3. Assert output shape and contents
        if result is None:
            raise ValueError("CT_PURE_BUILD_ETH_TRANSACTION_V0: internal error, result is None")
        
        if not isinstance(result, dict):
             raise ValueError(f"CT_PURE_BUILD_ETH_TRANSACTION_V0: internal error, result must be dict, got {type(result)}")
        
        if "unsigned_tx_bytes" not in result:
             raise ValueError("CT_PURE_BUILD_ETH_TRANSACTION_V0: internal error, missing 'unsigned_tx_bytes' in output")
        
        if result["unsigned_tx_bytes"] is None:
             raise ValueError("CT_PURE_BUILD_ETH_TRANSACTION_V0: internal error, output 'unsigned_tx_bytes' is None")

        return result

    except (ValueError, TypeError, KeyError) as e:
        # Re-raise with context instead of returning None or partial dict
        raise ValueError(f"CT_PURE_BUILD_ETH_TRANSACTION_V0: {str(e)}") from e


# --- Pure Python RLP Encoder ---


def _rlp_encode(item: Union[int, bytes, list]) -> bytes:
    """RLP encode a single item (integer, bytes, or list)."""
    if isinstance(item, list):
        return _rlp_encode_list(item)
    elif isinstance(item, (bytes, bytearray)):
        return _rlp_encode_bytes(item)
    elif isinstance(item, int):
        return _rlp_encode_integer(item)
    else:
        raise TypeError(f"RLP: unsupported type {type(item).__name__}")


def _rlp_encode_integer(value: int) -> bytes:
    """RLP encode a non-negative integer."""
    if value < 0:
        raise ValueError("RLP: negative integers not supported")
    if value == 0:
        return _rlp_encode_bytes(b"")
    return _rlp_encode_bytes(_int_to_big_endian(value))


def _rlp_encode_bytes(data: bytes) -> bytes:
    """RLP encode a byte string."""
    length = len(data)
    if length == 1 and data[0] < 0x80:
        return data
    elif length <= 55:
        return bytes([0x80 + length]) + data
    else:
        len_bytes = _int_to_big_endian(length)
        return bytes([0xB7 + len(len_bytes)]) + len_bytes + data


def _rlp_encode_list(items: list) -> bytes:
    """RLP encode a list of items."""
    encoded_items = b"".join(_rlp_encode(item) for item in items)
    length = len(encoded_items)
    if length <= 55:
        return bytes([0xC0 + length]) + encoded_items
    else:
        len_bytes = _int_to_big_endian(length)
        return bytes([0xF7 + len(len_bytes)]) + len_bytes + encoded_items


def _int_to_big_endian(value: int) -> bytes:
    """Convert a non-negative integer to big-endian bytes (no leading zeros)."""
    if value == 0:
        return b"\x00"
    byte_length = (value.bit_length() + 7) // 8
    return value.to_bytes(byte_length, byteorder="big")
