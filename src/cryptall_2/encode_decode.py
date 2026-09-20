import numpy as np

import os
from typing import Callable

from .helpers import (
    save_file_from_bites,
    load_file_to_bites,
    save_file_digests,
    add_noise,
    remove_noise,
    sudo_random_array,
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)
from .core.main_modulo import V5
from .core.sudo512_modulo import SUDO512_MOD
from .core.finite_field import F8
from .core.mutations.finite_field_mult_based import F8_MULT_BASED
from .core.mutations.finite_field_addition_based import F8_ADDITION_BASED
from .core.ring import RING
from .core.base import BaseEncodeDecodeAlgorithm


def _encode_pipeline(
    bites: np.ndarray,
    d_mod: int,
    seed: int,
    modifier_func: Callable[[np.ndarray], np.ndarray],
    algorithm_factory: Callable[[np.ndarray, np.ndarray], BaseEncodeDecodeAlgorithm],
    noise_ratio: float = 0.00,
    char_encode_mod: int = 256,
) -> np.ndarray:
    """Generic encoding pipeline to eliminate repeated boilerplate."""
    if noise_ratio > 0.0:
        bites = add_noise(bites, char_encode_mod, seed, noise_ratio)

    d_mod_range = randomize_d_mod(d_mod, seed)
    bites_mod = modifier_func(bites)
    algorithm = algorithm_factory(bites_mod, d_mod_range)
    return algorithm.encode()


def _decode_pipeline(
    bites: np.ndarray,
    d_mod: int,
    seed: int,
    algorithm_factory: Callable[[np.ndarray, np.ndarray], BaseEncodeDecodeAlgorithm],
    reverser_func: Callable[[np.ndarray], np.ndarray],
    noise_ratio: float = 0.00,
) -> np.ndarray:
    """Generic decoding pipeline to eliminate repeated boilerplate."""
    d_mod_range = randomize_d_mod(d_mod, seed)

    algorithm = algorithm_factory(bites, d_mod_range)
    decoded_bites = algorithm.decode()
    decoded_bites = reverser_func(decoded_bites)

    if noise_ratio > 0.0:
        decoded_bites = remove_noise(decoded_bites, noise_ratio)

    return decoded_bites


# --- IMPLEMENTATIONS ---


def encode_bites(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_sudo512_mod(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: SUDO512_MOD(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_sudo512_mod(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: SUDO512_MOD(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_f8(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: F8(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_f8(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: F8(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_f8_addition_based(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: F8_ADDITION_BASED(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_f8_addition_based(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: F8_ADDITION_BASED(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_f8_mult_based(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: F8_MULT_BASED(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


#


def decode_bites_f8_mult_based(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: F8_MULT_BASED(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_ring(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: RING(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_ring(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: RING(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_rand(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
    )


def decode_bites_rand(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
    )


def encode_bites_full(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_full_vector(b),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
    )


def decode_bites_full(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_full_vector(b),
    )


if __name__ == "__main__":
    image_name = "img.jpg"
    # "C:\Users\Timofii\code\python\cryptall_2\tests\test_results\encoded\img_encoded.jpg"
    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"
    save_file_digests(file_path, save_file_path)
