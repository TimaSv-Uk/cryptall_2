from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtGui import QAction, QIntValidator, QFont, QTextCursor

from pathlib import Path

from cryptall_2.encode_decode_file import AlgorithmType


from ..constants import DEFAULT_SEED
from ..decode_worker import DecodeWorker
from ..encode_worker import EncodeWorker
from ..languages.ui_language_manager import UILanguageManager



class FormOriginal(QtWidgets.QWidget):
    def set_algoirithm_title(self) -> None:  
        json_path = "main_page.algorithm_title.default"
        self.algorithm_title = self.lang_text.get(json_path)
        if hasattr(self, 'subtitle'):
            self.subtitle.setText(self.algorithm_title)

    def __init__(self, lang_text:UILanguageManager):
        super().__init__()
        self.lang_text = lang_text
        self.algorithm_type = AlgorithmType.V5
        self.set_algoirithm_title()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.title = QtWidgets.QLabel(
            self.lang_text.get("main_page.title"), alignment=QtCore.Qt.AlignCenter
        )
        self.title.setObjectName("titleLabel")
        layout.addWidget(self.title)
        # Subtitle / Algorithm Title (Placed right under main title)
        self.subtitle = QtWidgets.QLabel(
            self.algorithm_title, alignment=QtCore.Qt.AlignCenter
        )
        self.subtitle.setObjectName("algorithmTitleLabel")
        layout.addWidget(self.subtitle)
        # File Selection Group
        self.file_group = QGroupBox(
            self.lang_text.get("main_page.file_selection.group_title")
        )
        file_layout = QVBoxLayout(self.file_group)

        self.file_button = QtWidgets.QPushButton(
            self.lang_text.get("main_page.file_selection.button")
        )
        self.file_label = QtWidgets.QLabel(
            self.lang_text.get("main_page.file_selection.no_file")
        )
        self.file_label.setWordWrap(True)
        self.file_button.clicked.connect(self.open_file_dialog)
        self.file_lineedit = QtWidgets.QLineEdit()
        self.file_lineedit.setPlaceholderText(
            self.lang_text.get("main_page.file_selection.placeholder")
        )
        self.file_lineedit.textChanged.connect(
            lambda text: self.file_label.setText(text)
        )

        file_layout.addWidget(self.file_lineedit)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)

        # Number Input Group
        self.seed_group = QGroupBox(
            self.lang_text.get("main_page.configuration.group_title")
        )
        seed_layout = QVBoxLayout(self.seed_group)

        self.seed_input = QtWidgets.QLineEdit()
        self.seed_input.setPlaceholderText(
            self.lang_text.get(
                "main_page.configuration.placeholder", default=DEFAULT_SEED
            )
        )
        self.seed_input.setValidator(QIntValidator())
        seed_layout.addWidget(self.seed_input)

        # Save Path Group
        self.save_group = QGroupBox(self.lang_text.get("main_page.output.group_title"))
        save_layout = QVBoxLayout(self.save_group)

        self.save_lineedit = QtWidgets.QLineEdit()
        self.save_lineedit.setPlaceholderText(
            self.lang_text.get("main_page.output.placeholder")
        )
        self.save_lineedit.textChanged.connect(
            lambda text: self.save_label.setText(text)
        )

        self.save_button = QtWidgets.QPushButton(
            self.lang_text.get("main_page.output.button")
        )
        self.save_label = QtWidgets.QLabel(
            self.lang_text.get("main_page.output.no_path")
        )
        self.save_label.setWordWrap(True)
        self.save_button.clicked.connect(self.open_save_dialog)

        save_layout.addWidget(self.save_lineedit)
        save_layout.addWidget(self.save_button)
        save_layout.addWidget(self.save_label)

        # Action Buttons Group
        self.action_group = QGroupBox(
            self.lang_text.get("main_page.actions.group_title")
        )
        action_layout = QHBoxLayout(self.action_group)

        self.encode_button = QtWidgets.QPushButton(
            self.lang_text.get("main_page.actions.encode_button")
        )
        self.decode_button = QtWidgets.QPushButton(
            self.lang_text.get("main_page.actions.decode_button")
        )
        self.swap_encode_decode_file_button = QtWidgets.QPushButton(
            self.lang_text.get("main_page.actions.swap_button")
        )

        self.encode_button.clicked.connect(self.encode_file_action)
        self.decode_button.clicked.connect(self.decode_file_action)
        self.swap_encode_decode_file_button.clicked.connect(
            self.swap_encode_decode_file
        )

        action_layout.addWidget(self.encode_button)
        action_layout.addWidget(self.decode_button)
        action_layout.addWidget(self.swap_encode_decode_file_button)

        # Status Display
        self.status_text = QtWidgets.QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(100)
        self.status_text.setMaximumHeight(200)
        self.status_text.setPlaceholderText(
            self.lang_text.get("main_page.status.placeholder")
        )

        # Add all groups to main layout
        layout.addWidget(self.file_group)
        layout.addWidget(self.seed_group)
        layout.addWidget(self.save_group)
        layout.addWidget(self.action_group)
        layout.addWidget(self.status_text)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self.lang_text.get("main_page.dialogs.select_file"),
            str(Path.home()),  # Default to user's home directory safely
            self.lang_text.get("main_page.dialogs.all_files"),
        )
        if filename:
            # Normalize path slashes for the current OS
            norm_path = str(Path(filename).resolve())
            self.file_label.setText(norm_path)
            self.file_lineedit.setText(norm_path)
            self.update_status(
                self.lang_text.get("main_page.status.file_selected", path=norm_path)
            )

    def open_save_dialog(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            self.lang_text.get("main_page.dialogs.select_save"),
            str(Path.home()),  # Default to user's home directory safely
            self.lang_text.get("main_page.dialogs.all_files"),
        )
        if save_path:
            # Normalize path slashes for the current OS
            norm_path = str(Path(save_path).resolve())
            self.save_label.setText(norm_path)
            self.save_lineedit.setText(norm_path)
            self.update_status(
                self.lang_text.get("main_page.status.save_path_set", path=norm_path)
            )

    def swap_encode_decode_file(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()

        no_file = self.lang_text.get("main_page.file_selection.no_file")
        no_path = self.lang_text.get("main_page.output.no_path")

        if self.file_lineedit.text() == "" or self.save_lineedit.text() == "":
            if file_path == no_file or save_path == no_path:
                return

        self.file_label.setText(save_path)
        self.save_label.setText(file_path)

        self.file_lineedit.setText(save_path)
        self.save_lineedit.setText(file_path)

        self.update_status(
            self.lang_text.get(
                "main_page.status.swap", path1=save_path, path2=file_path
            )
        )

    def update_status(self, message):
        current_text = self.status_text.toPlainText()
        if current_text:
            new_text = current_text + "\n" + message
        else:
            new_text = message
        self.status_text.setPlainText(new_text)
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)

    def validate_inputs(self):
        file_path = self.file_label.text()
        save_path = self.save_label.text()

        if self.file_lineedit.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                self.lang_text.get("main_page.warnings.invalid_input"),
                self.lang_text.get("main_page.warnings.no_file_selected"),
            )
            return None, None, None

        # Robust cross-platform existence check
        if not Path(file_path).exists():
            QtWidgets.QMessageBox.warning(
                self,
                self.lang_text.get("main_page.warnings.invalid_input"),
                self.lang_text.get("main_page.warnings.file_not_exist", path=file_path),
            )
            return None, None, None

        if file_path == save_path:
            QtWidgets.QMessageBox.warning(
                self,
                self.lang_text.get("main_page.warnings.invalid_input"),
                self.lang_text.get("main_page.warnings.same_paths"),
            )
            return None, None, None

        if self.save_lineedit.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                self.lang_text.get("main_page.warnings.invalid_input"),
                self.lang_text.get("main_page.warnings.no_save_path"),
            )
            return None, None, None

        seed_input_text = self.seed_input.text()
        seed = int(seed_input_text) if seed_input_text else DEFAULT_SEED

        return file_path, save_path, seed

    def encode_file_action(self):
        file_path, save_path, seed = self.validate_inputs()
        if file_path is None:
            return

        try:
            self.loader = QtWidgets.QProgressDialog(
                self.lang_text.get("main_page.dialogs.encoding"), None, 0, 0, self
            )
            self.loader.setWindowTitle(
                self.lang_text.get("main_page.dialogs.please_wait")
            )
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()

            self.worker = EncodeWorker(
                file_path, save_path, seed, self.lang_text, self.algorithm_type
            )
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(self.lang_text.get("main_page.status.encoded"))
            self.update_status(
                self.lang_text.get("main_page.status.input", path=file_path)
            )
            self.update_status(
                self.lang_text.get("main_page.status.output", path=save_path)
            )
            if seed != DEFAULT_SEED:
                self.update_status(
                    self.lang_text.get("main_page.status.number", number=seed)
                )

        except Exception as e:
            self.update_status(
                self.lang_text.get("main_page.status.error", error=str(e))
            )

    def decode_file_action(self):
        file_path, save_path, number = self.validate_inputs()
        if file_path is None:
            return

        try:
            self.loader = QtWidgets.QProgressDialog(
                self.lang_text.get("main_page.dialogs.decoding"), None, 0, 0, self
            )
            self.loader.setWindowTitle(
                self.lang_text.get("main_page.dialogs.please_wait")
            )
            self.loader.setWindowModality(QtCore.Qt.WindowModal)
            self.loader.setCancelButton(None)
            self.loader.show()

            self.worker = DecodeWorker(
                file_path, save_path, number, self.lang_text, self.algorithm_type
            )
            self.worker.finished.connect(self.on_done)
            self.worker.start()

            self.update_status(self.lang_text.get("main_page.status.decoded"))
            self.update_status(
                self.lang_text.get("main_page.status.input", path=file_path)
            )
            self.update_status(
                self.lang_text.get("main_page.status.output", path=save_path)
            )
            if number != DEFAULT_SEED:
                self.update_status(
                    self.lang_text.get("main_page.status.number", number=number)
                )

        except Exception as e:
            self.update_status(
                self.lang_text.get("main_page.status.error", error=str(e))
            )

    def on_done(self, success, message):
        self.loader.close()
        if success:
            QtWidgets.QMessageBox.information(
                self, self.lang_text.get("main_page.dialogs.success"), message
            )
        else:
            QtWidgets.QMessageBox.critical(
                self, self.lang_text.get("main_page.dialogs.error"), message
            )

    def refresh_ui(self):

        self.set_algoirithm_title()

        self.title.setText(self.lang_text.get("main_page.title"))
        self.file_group.setTitle(
            self.lang_text.get("main_page.file_selection.group_title")
        )
        self.seed_group.setTitle(
            self.lang_text.get("main_page.configuration.group_title")
        )
        self.save_group.setTitle(self.lang_text.get("main_page.output.group_title"))
        self.action_group.setTitle(self.lang_text.get("main_page.actions.group_title"))

        self.file_button.setText(self.lang_text.get("main_page.file_selection.button"))
        self.save_button.setText(self.lang_text.get("main_page.output.button"))
        self.encode_button.setText(
            self.lang_text.get("main_page.actions.encode_button")
        )
        self.decode_button.setText(
            self.lang_text.get("main_page.actions.decode_button")
        )
        self.swap_encode_decode_file_button.setText(
            self.lang_text.get("main_page.actions.swap_button")
        )

        self.file_lineedit.setPlaceholderText(
            self.lang_text.get("main_page.file_selection.placeholder")
        )
        self.seed_input.setPlaceholderText(
            self.lang_text.get(
                "main_page.configuration.placeholder", default=DEFAULT_SEED
            )
        )
        self.save_lineedit.setPlaceholderText(
            self.lang_text.get("main_page.output.placeholder")
        )
        self.status_text.setPlaceholderText(
            self.lang_text.get("main_page.status.placeholder")
        )

        if not self.file_lineedit.text():
            self.file_label.setText(
                self.lang_text.get("main_page.file_selection.no_file")
            )
        if not self.save_lineedit.text():
            self.save_label.setText(self.lang_text.get("main_page.output.no_path"))
