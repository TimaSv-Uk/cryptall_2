from cryptall_2.encode_decode_file import AlgorithmType

from .original import FormOriginal

class FormSudo512Modulo(FormOriginal): 

    """
    Main changes front 
     def encode_bites_sudo512_mod(
         bites: np.ndarray,
         char_encode_mod: int,
         d_mod: int,
         seed: int,
         noise_ratio: float = 0.00,
     ) -> np.ndarray:

     def decode_bites_sudo512_mod(
         bites: np.ndarray,
         char_encode_mod: int,
         d_mod: int,
         seed: int,
         noise_ratio: float = 0.00,
     ) -> np.ndarray:
    """
    def __init__(self):
        super().__init__()
        self.algorithm_type = AlgorithmType.SUDO512_MOD

