from cryptall_2.encode_decode import encode_file, decode_file

from PySide6 import QtCore

class EncodeWorker(QtCore.QThread):
    finished = QtCore.Signal(bool, str)

    def __init__(self, file_path: str, save_path: str, seed: int, tr):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.seed = seed
        self.tr = tr

    def run(self):
        try:
            encode_file(self.file_path, self.save_path, self.seed)
            msg = self.tr.get("main_page.dialogs.file_encoded", seed=self.seed)
            self.finished.emit(True, msg)
        except Exception as e:
            self.finished.emit(False, str(e))

