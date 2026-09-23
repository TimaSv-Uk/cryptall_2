from cryptall_2.encode_decode_file import decode_file, AlgorithmType

from PySide6 import QtCore

class DecodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(
        self,
        file_path: str,
        save_path: str,
        seed: int,
        tr,
        algorithm: AlgorithmType = AlgorithmType.V5
    ):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.algorithm = algorithm
        self.seed = seed
        self.tr = tr

    def run(self):
        try:
            decode_file(self.file_path, self.save_path, self.seed, self.algorithm)
            msg = self.tr.get("main_page.dialogs.file_decoded", seed=self.seed)
            self.finished.emit(True, msg)
        except Exception as e:
            self.finished.emit(False, str(e))
