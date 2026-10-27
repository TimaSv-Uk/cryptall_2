import numpy as np
import galois
import numpy as np

from typing import Callable
from dataclasses import dataclass

from .helpers import (
    save_file_digests,
    add_noise,
    remove_noise,
    change_first_symbol_based_on_random_vector,
    load_file_to_bites,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)
from .core.mutations.finite_field_mult_based import F8_MULT_BASED
from .core.base import BaseEncodeDecodeAlgorithm
from .precompute_multiplication import load_gf256

# NOTE: this is public key implementation of ecode_decode

@dataclass(frozen=True)
class DecodeKey:
    pk_transformed: np.ndarray
    m_inv: np.ndarray  

    def recover(self) -> np.ndarray:
        gf = GF256
        return np.array(gf(self.m_inv) @ gf(self.pk_transformed), dtype=np.uint8)

# Initialize the Galois Field GF(2^8)
GF256 = galois.GF(2**8)

def encode_bites_f8_mult_based_publickey(
    bites: np.ndarray,
    d_mod: int,
    encode_key: int,
    noise_ratio: float = 0.00,
):
    d_mod_range = randomize_d_mod(d_mod, encode_key)  # PRIVATE, never shared
    mul_lut = load_gf256()

    bites_mod = bites
    if noise_ratio > 0.0:
        bites_mod = add_noise(bites_mod, 256, encode_key, noise_ratio)

    algorithm = F8_MULT_BASED(bites_mod, d_mod_range)
    encoded = algorithm.encode()

    public_key = get_public_key(d_mod_range, mul_lut)  # SHARED public key
    return encoded, public_key


def decode_bites_f8_mult_based_publickey(
    bites: np.ndarray,
    public_key: np.ndarray,
    noise_ratio: float = 0.00,
):
    algorithm = F8_MULT_BASED(bites, public_key)
    decoded_bites = algorithm.decode(precomputed_inverses=public_key)

    if noise_ratio > 0.0:
        decoded_bites = remove_noise(decoded_bites, noise_ratio)

    return decoded_bites

def get_public_key(d_mod_range: np.ndarray, mul_lut: np.ndarray) -> np.ndarray:
    """
    Derive the public decode key from the private encode sequence.
    Each element is the GF(2^8) multiplicative inverse of the
    corresponding private a-value used during encoding.
    """
    public_key = np.zeros_like(d_mod_range, dtype=np.uint8)
    for i in range(len(d_mod_range)):
        a_raw = d_mod_range[i]
        a = np.uint8(1) if a_raw == 0 else np.uint8(a_raw)
        public_key[i] = np.where(mul_lut[a] == 1)[0][0]
    return public_key

def get_public_key_with_linear_transform(
    d_mod_range: np.ndarray, mul_lut: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates the public key and applies a linear transformation (matrix multiplication by M)
    using the Galois field library.
    """
    public_key_raw = get_public_key(d_mod_range, mul_lut)

    n = len(public_key_raw)
    
    # If the key is too short for a full matrix, return as is
    if n < 2:
        return public_key_raw, np.array([[1]], dtype=np.uint8)

    # Create a random invertible transformation matrix M of size n x n in GF(2^8)
    while True:
        M_np = np.random.randint(0, 256, size=(n, n), dtype=np.uint8)
        M = GF256(M_np)
        # Check if the matrix is invertible or generate a new one 
        try:
            M_inv = np.linalg.inv(M)
            break
        except np.linalg.LinAlgError:
            continue  

    # Convert the public key to a Galois field array and apply the linear transformation
    pk_gf = GF256(public_key_raw)
    pk_transformed = M @ pk_gf  # Superposition / linear transformation

    return np.array(pk_transformed, dtype=np.uint8), np.array(M_inv, dtype=np.uint8)


def encode_bites_f8_mult_based_publickey_transformed(
    bites: np.ndarray,
    d_mod: int,
    encode_key: int,
    noise_ratio: float = 0.00,
) -> tuple[np.ndarray, DecodeKey]:
    d_mod_range = randomize_d_mod(d_mod, encode_key)  # PRIVATE, never shared
    mul_lut = load_gf256()

    bites_mod = bites
    if noise_ratio > 0.0:
        bites_mod = add_noise(bites_mod, 256, encode_key, noise_ratio)

    algorithm = F8_MULT_BASED(bites_mod, d_mod_range)
    encoded = algorithm.encode()

    pk_transformed, M_inv = get_public_key_with_linear_transform(d_mod_range, mul_lut)  # SHARED public key
    
    return encoded, DecodeKey(pk_transformed, M_inv)

def decode_bites_f8_mult_based_publickey_transformed(
    bites: np.ndarray,
    public_key_transformed: DecodeKey,
    noise_ratio: float = 0.00,
) -> np.array:

    """
    Decodes data using a transformed public key by first reversing the linear transformation
    with the inverse matrix M_inv.
    """
    #  Restore the original public key using the inverse matrix

    original_pk = public_key_transformed.recover()

    decoded_bites = decode_bites_f8_mult_based_publickey(bites, original_pk, noise_ratio)

    return decoded_bites

if __name__ == "__main__":
    image_name = "img.jpg"
    # "C:\Users\Timofii\code\python\cryptall_2\tests\test_results\encoded\img_encoded.jpg"
    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"
