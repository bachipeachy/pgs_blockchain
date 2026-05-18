"""
CT_PURE_DERIVE_WALLET_KEYPAIRS_V0

Pure Capability Transform (Atom)

Purpose:
    Generate entropy, derive HD wallet keys, and produce dual-address
    keypairs (EOA + UTXO) from a single seed. Returns only
    public-derivable fields. Private material stays in function scope
    and is never returned.

Implementation:
    - Uses bip_utils for BIP32/BIP39 derivation
    - Uses cryptography for public key derivation
    - Uses Crypto.Hash.keccak for Ethereum address derivation
    - Uses hashlib for HASH160 master fingerprint

Security invariant:
    No output field contains private_key, seed, mnemonic, or entropy.
    These exist only within this function's scope and are discarded on return.
"""

import hashlib
import os
from typing import Dict, Any, List

from bip_utils import (
    Bip32Secp256k1,
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip39MnemonicValidator,
    Bip39Languages,
)
from Crypto.Hash import keccak
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


_ALLOWED_ENTROPY_BITS = {128, 160, 192, 224, 256}


def _path_to_string(root_indices: List[int], child_indices: List[int]) -> str:
    """Convert path indices to BIP32 path string (e.g., m/44'/66'/0'/0/0)."""
    parts = ["m"]
    for idx in root_indices:
        if idx >= 0x80000000:
            parts.append(f"{idx - 0x80000000}'")
        else:
            parts.append(str(idx))
    for idx in child_indices:
        if idx >= 0x80000000:
            parts.append(f"{idx - 0x80000000}'")
        else:
            parts.append(str(idx))
    return "/".join(parts)


def _derive_public_key_bytes(private_key_raw: bytes, curve_name: str) -> bytes:
    """Derive uncompressed public key from raw private key bytes."""
    if curve_name == "secp256k1":
        curve = ec.SECP256K1()
    elif curve_name == "secp256r1":
        curve = ec.SECP256R1()
    else:
        raise ValueError(f"Unsupported curve: {curve_name}")

    private_key = ec.derive_private_key(
        int.from_bytes(private_key_raw, byteorder="big"),
        curve,
        default_backend(),
    )
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )


def _pubkey_to_eth_address(pubkey_uncompressed: bytes) -> str:
    """Derive Ethereum address from uncompressed public key."""
    raw_pub = pubkey_uncompressed[1:]  # Remove 0x04 prefix
    k = keccak.new(digest_bits=256)
    k.update(raw_pub)
    return "0x" + k.digest()[-20:].hex()


def _compute_master_fingerprint(master_bip32) -> str:
    """Compute HASH160 fingerprint of master public key (first 4 bytes, hex)."""
    compressed_pubkey = master_bip32.PublicKey().RawCompressed().ToBytes()
    sha256 = hashlib.sha256(compressed_pubkey).digest()
    ripemd160 = hashlib.new("ripemd160", sha256).digest()
    return ripemd160[:4].hex()


def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Execute CT_PURE_DERIVE_WALLET_KEYPAIRS_V0.

    Inputs:
        entropy_bits (int): Entropy strength (128, 160, 192, 224, 256)
        passphrase (str): BIP39 passphrase (default "")
        root_path_indices (list[int]): Hardened root path indices (e.g., [0x8000002C, 0x80000042, 0x80000000])
        eoa_child_indices (list[int]): EOA child path indices (e.g., [0, 0])
        utxo_child_indices (list[int]): UTXO child path indices (e.g., [1, 0])
        curve (str): Elliptic curve name (default "secp256k1")

    Outputs:
        eoa_public_key_hex (str): EOA uncompressed public key, hex
        eoa_address (str): EOA Ethereum address, 0x-prefixed hex
        eoa_derivation_path (str): Full EOA BIP32 path string
        utxo_public_key_hex (str): UTXO uncompressed public key, hex
        utxo_address (str): UTXO Ethereum address, 0x-prefixed hex
        utxo_derivation_path (str): Full UTXO BIP32 path string
        master_fingerprint (str): HASH160(master_pubkey)[:4], hex
    """
    # ---- Input validation ----
    for required in ("entropy_bits", "root_path_indices", "eoa_child_indices", "utxo_child_indices"):
        if required not in inputs:
            raise ValueError(f"CT_PURE_DERIVE_WALLET_KEYPAIRS_V0: missing required input '{required}'")

    entropy_bits = inputs["entropy_bits"]
    passphrase = inputs.get("passphrase", "")
    root_path_indices = inputs["root_path_indices"]
    eoa_child_indices = inputs["eoa_child_indices"]
    utxo_child_indices = inputs["utxo_child_indices"]
    curve_name = inputs.get("curve", "secp256k1")

    if not isinstance(entropy_bits, int) or entropy_bits not in _ALLOWED_ENTROPY_BITS:
        raise ValueError(
            f"CT_PURE_DERIVE_WALLET_KEYPAIRS_V0: entropy_bits must be one of {sorted(_ALLOWED_ENTROPY_BITS)}"
        )

    for name, indices in [("root_path_indices", root_path_indices),
                          ("eoa_child_indices", eoa_child_indices),
                          ("utxo_child_indices", utxo_child_indices)]:
        if not isinstance(indices, (list, tuple)):
            raise TypeError(f"CT_PURE_DERIVE_WALLET_KEYPAIRS_V0: {name} must be a list")
        for idx in indices:
            if not isinstance(idx, int) or idx < 0 or idx > 0xFFFFFFFF:
                raise ValueError(f"CT_PURE_DERIVE_WALLET_KEYPAIRS_V0: {name} contains invalid index: {idx}")

    # ---- Step 1: Generate or accept entropy ----
    entropy_bytes_input = inputs.get("entropy_bytes")
    if entropy_bytes_input is not None:
        # Injected entropy for deterministic testing (hex string, with or without 0x prefix)
        hex_str = entropy_bytes_input if isinstance(entropy_bytes_input, str) else entropy_bytes_input.hex()
        if hex_str.startswith("0x") or hex_str.startswith("0X"):
            hex_str = hex_str[2:]
        entropy_bytes = bytes.fromhex(hex_str)
        if len(entropy_bytes) != entropy_bits // 8:
            raise ValueError(
                f"CT_PURE_DERIVE_WALLET_KEYPAIRS_V0: entropy_bytes length {len(entropy_bytes)} "
                f"does not match entropy_bits {entropy_bits} ({entropy_bits // 8} bytes expected)"
            )
    else:
        entropy_bytes = os.urandom(entropy_bits // 8)

    # ---- Step 2: Entropy → mnemonic ----
    mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromEntropy(entropy_bytes).ToStr()

    # ---- Step 3: Mnemonic → seed ----
    seed_bytes = bytes(Bip39SeedGenerator(mnemonic, Bip39Languages.ENGLISH).Generate(passphrase))

    # ---- Step 4: Seed → master key ----
    bip32_master = Bip32Secp256k1.FromSeed(seed_bytes)

    # ---- Step 5: Master fingerprint ----
    master_fingerprint = _compute_master_fingerprint(bip32_master)

    # ---- Step 6: Derive root path (e.g., m/44'/66'/0') ----
    bip32_root = bip32_master
    for idx in root_path_indices:
        bip32_root = bip32_root.ChildKey(idx)

    # ---- Step 7: Derive EOA child (e.g., 0/0) ----
    bip32_eoa = bip32_root
    for idx in eoa_child_indices:
        bip32_eoa = bip32_eoa.ChildKey(idx)

    eoa_private_raw = bip32_eoa.PrivateKey().Raw().ToBytes()
    eoa_pubkey_bytes = _derive_public_key_bytes(eoa_private_raw, curve_name)
    eoa_address = _pubkey_to_eth_address(eoa_pubkey_bytes)
    eoa_path = _path_to_string(root_path_indices, eoa_child_indices)

    # ---- Step 8: Derive UTXO child (e.g., 1/0) ----
    bip32_utxo = bip32_root
    for idx in utxo_child_indices:
        bip32_utxo = bip32_utxo.ChildKey(idx)

    utxo_private_raw = bip32_utxo.PrivateKey().Raw().ToBytes()
    utxo_pubkey_bytes = _derive_public_key_bytes(utxo_private_raw, curve_name)
    utxo_address = _pubkey_to_eth_address(utxo_pubkey_bytes)
    utxo_path = _path_to_string(root_path_indices, utxo_child_indices)

    # ---- Return ONLY public-derivable fields ----
    # Private keys, mnemonic, seed, and entropy stay in this function's scope
    # and are discarded when the function returns.
    return {
        "eoa_public_key_hex": eoa_pubkey_bytes.hex(),
        "eoa_address": eoa_address,
        "eoa_derivation_path": eoa_path,
        "utxo_public_key_hex": utxo_pubkey_bytes.hex(),
        "utxo_address": utxo_address,
        "utxo_derivation_path": utxo_path,
        "master_fingerprint": master_fingerprint,
    }
