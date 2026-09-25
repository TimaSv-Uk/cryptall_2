from cryptall_2.encode_decode_file import AlgorithmType

from .original import FormOriginal
from ..languages.ui_language_manager import UILanguageManager

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

    def set_algoirithm_title(self) -> None:  
        json_path = "main_page.algorithm_title.form_sudo512modulo"
        self.algorithm_title = self.lang_text.get(json_path)
        if hasattr(self, 'subtitle'):
            self.subtitle.setText(self.algorithm_title)

    def __init__(self,lang_text:UILanguageManager):
        super().__init__(lang_text)
        self.algorithm_type = AlgorithmType.SUDO512_MOD

