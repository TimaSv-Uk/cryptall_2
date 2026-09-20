from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Union

import numpy as np

from .helpers import (
    save_file_from_bites,
    load_file_to_bites,
)

from cryptall_2.encode_decode import (
    encode_bites,
    decode_bites,
    encode_bites_rand,
    encode_bites_full,
    encode_bites_ring,
    decode_bites_ring,
    remove_noise,
    decode_bites_rand,
    encode_bites_f8,
    decode_bites_f8,
    encode_bites_sudo512_mod,
    decode_bites_sudo512_mod,
    decode_bites_full,
    encode_bites_f8_addition_based,
    decode_bites_f8_addition_based,
    encode_bites_f8_mult_based,
    decode_bites_f8_mult_based,
)


CHAR_ENCODE_MOD = 256
D_MOD = 128


class AlgorithmType(str, Enum):
    V5 = "v5"
    V5_RAND = "v5_rand"
    V5_FULL = "v5_full"
    RING = "ring"
    F8 = "f8"
    F8_ADDITION = "f8_addition"
    F8_MULT = "f8_mult"
    SUDO512_MOD = "sudo512_mod"


@dataclass(frozen=True)
class AlgorithmSpec:
    encode: Callable[..., np.ndarray]
    decode: Callable[..., np.ndarray]
    supports_noise: bool = True  # *_rand / *_full don't accept noise_ratio


_REGISTRY: Dict[AlgorithmType, AlgorithmSpec] = {
    AlgorithmType.V5: AlgorithmSpec(encode_bites, decode_bites),
    AlgorithmType.V5_RAND: AlgorithmSpec(
        encode_bites_rand, decode_bites_rand, supports_noise=False
    ),
    AlgorithmType.V5_FULL: AlgorithmSpec(
        encode_bites_full, decode_bites_full, supports_noise=False
    ),
    AlgorithmType.RING: AlgorithmSpec(encode_bites_ring, decode_bites_ring),
    AlgorithmType.F8: AlgorithmSpec(encode_bites_f8, decode_bites_f8),
    AlgorithmType.F8_ADDITION: AlgorithmSpec(
        encode_bites_f8_addition_based, decode_bites_f8_addition_based
    ),
    AlgorithmType.F8_MULT: AlgorithmSpec(
        encode_bites_f8_mult_based, decode_bites_f8_mult_based
    ),
    AlgorithmType.SUDO512_MOD: AlgorithmSpec(
        encode_bites_sudo512_mod, decode_bites_sudo512_mod
    ),
}


def _call(fn, spec: AlgorithmSpec, bites, seed: int, noise_ratio: float):
    kwargs = {}
    if spec.supports_noise:
        kwargs["noise_ratio"] = noise_ratio
    elif noise_ratio > 0.0:
        raise ValueError("This algorithm does not support noise_ratio")
    return fn(bites, CHAR_ENCODE_MOD, D_MOD, seed, **kwargs)


def encode_file(
    file_path: str,
    save_encoded_file_path: str,
    seed: int = 42,
    algorithm: AlgorithmType = AlgorithmType.V5,
    noise_ratio: float = 0.0,
):
    spec = _REGISTRY[algorithm]
    file_bites = load_file_to_bites(file_path)
    encoded = _call(spec.encode, spec, file_bites, seed, noise_ratio)
    save_file_from_bites(save_encoded_file_path, encoded)


def decode_file(
    encoded_file_path: str,
    save_decoded_file_path: str,
    seed: int = 42,
    algorithm: AlgorithmType = AlgorithmType.V5,
    noise_ratio: float = 0.0,
):
    spec = _REGISTRY[algorithm]
    file_bites = load_file_to_bites(encoded_file_path)
    decoded = _call(spec.decode, spec, file_bites, seed, noise_ratio)
    save_file_from_bites(save_decoded_file_path, decoded)


# Usage:
#   encode_file("in.bin", "out.enc", seed=7, algorithm=AlgorithmType.RING)
#   decode_file("out.enc", "back.bin", seed=7, algorithm=AlgorithmType.RING)
