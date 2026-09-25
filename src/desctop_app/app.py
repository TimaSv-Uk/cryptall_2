from PySide6 import QtCore, QtWidgets

from PySide6.QtGui import QAction

import sys
from pathlib import Path

from .pages.page_one import PageOne
from .pages.page_two import PageTwo
from .forms.original import FormOriginal
from .forms.sudo512_modulo import FormSudo512Modulo
from .languages.ui_language_manager import UILanguageManager

from .constants import DEFAULT_SEED


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, tr: UILanguageManager, lang_dir: str):
        super().__init__()
        self.tr = tr
        self.lang_dir = Path(lang_dir)
        self.setWindowTitle(self.tr.get("window_title"))

        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()

        self.page_width = int(screen_width * 0.70)

        self.form_original = FormOriginal(tr)
        self.form_sudo = FormSudo512Modulo(tr)

        self.algorithm_stack = QtWidgets.QStackedWidget()
        self.algorithm_stack.addWidget(self.form_original)  # Index 0
        self.algorithm_stack.addWidget(self.form_sudo)  # Index 1

        self.page_one = PageOne(tr)
        self.page_two = PageTwo(tr)
        self.page_one = PageOne(tr)
        self.page_two = PageTwo(tr)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.algorithm_stack)
        self.stacked_widget.addWidget(self.page_one)
        self.stacked_widget.addWidget(self.page_two)
        self.stacked_widget.setMaximumSize(self.page_width, 1100)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        scroll.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        scroll.setFixedWidth(self.page_width)

        scroll.setWidget(self.stacked_widget)

        central_container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(central_container)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(scroll)
        h_layout.addStretch(1)
        container_layout.addLayout(h_layout)

        self.setCentralWidget(central_container)

        menu_bar = self.menuBar()

        self.algo_menu = menu_bar.addMenu(
            self.tr.get("menu.algorithms", default="Algorithms")
        )

        self.action_original = QAction("Original", self)
        self.action_sudo = QAction("Sudo 512 Modulo", self)

        self.algo_menu.addAction(self.action_original)
        self.algo_menu.addAction(self.action_sudo)

        # When an algorithm is selected, change the nested stack AND ensure we are on the main page view
        self.action_original.triggered.connect(self.show_original_algorithm)
        self.action_sudo.triggered.connect(self.show_sudo_algorithm)

        self.navigate_menu = menu_bar.addMenu(self.tr.get("menu.menu"))

        self.main_action = QAction(self.tr.get("menu.main_page"), self)
        self.docs_action = QAction(self.tr.get("menu.documentation"), self)
        self.about_action = QAction(self.tr.get("menu.about"), self)

        self.navigate_menu.addAction(self.main_action)
        self.navigate_menu.addAction(self.docs_action)
        self.navigate_menu.addAction(self.about_action)

        self.main_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        self.docs_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )
        self.about_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(2)
        )

        self.language_menu = menu_bar.addMenu(self.tr.get("language_menu"))
        self.create_language_menu()

        self.apply_styles()

    def create_language_menu(self):
        self.language_menu.clear()

        if not self.lang_dir.exists():
            no_lang_action = QAction("No languages folder found", self)
            no_lang_action.setEnabled(False)
            self.language_menu.addAction(no_lang_action)
            return

        lang_files = [
            f for f in self.lang_dir.iterdir() if f.is_file() and f.suffix == ".json"
        ]

        if not lang_files:
            no_lang_action = QAction("No language files found", self)
            no_lang_action.setEnabled(False)
            self.language_menu.addAction(no_lang_action)
            return

        for lang_path in sorted(lang_files):
            lang_name = lang_path.stem.upper()
            abs_lang_path = str(lang_path.resolve())

            lang_action = QAction(lang_name, self)
            lang_action.setCheckable(True)

            if abs_lang_path == self.tr.current_lang_file:
                lang_action.setChecked(True)

            lang_action.triggered.connect(
                lambda checked, path=abs_lang_path: self.change_language(path)
            )
            self.language_menu.addAction(lang_action)

    def change_language(self, lang_file):
        try:
            self.tr.load_language(lang_file)
            self.refresh_all_ui()
            self.create_language_menu()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to load language file:\n{str(e)}"
            )

    def refresh_all_ui(self):
        self.setWindowTitle(self.tr.get("window_title"))

        self.navigate_menu.setTitle(self.tr.get("menu.menu"))
        self.main_action.setText(self.tr.get("menu.main_page"))
        self.docs_action.setText(self.tr.get("menu.documentation"))
        self.about_action.setText(self.tr.get("menu.about"))


        self.algo_menu.setTitle(self.tr.get("menu.algorithms", default="Algorithms"))
        self.action_original.setText(self.tr.get("algo.original", default="Original"))
        self.action_sudo.setText(self.tr.get("algo.sudo", default="Sudo 512 Modulo"))

        self.language_menu.setTitle(self.tr.get("language_menu"))

        self.form_original.refresh_ui()
        self.form_sudo.refresh_ui()

        self.page_one.refresh_ui()
        self.page_two.refresh_ui()

    def show_original_algorithm(self):
        self.algorithm_stack.setCurrentIndex(0)
        self.stacked_widget.setCurrentIndex(
            0
        )  # Forces view back to main page if user was in Docs/About

    def show_sudo_algorithm(self):
        self.algorithm_stack.setCurrentIndex(1)
        self.stacked_widget.setCurrentIndex(
            0
        )  # Forces view back to main page if user was in Docs/About

    def apply_styles(self):
        self.setStyleSheet("""
            * {
                font-size: 20px;

                font-family: monospace;
            }
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QStackedWidget {
                background-color: #ffffff;
                border: none;
            }
            QLabel {
                color: #000000;
                padding: 5px;
            }
            #titleLabel {
                font-size: 42px;
                font-weight: bold;
            }
            #algorithmTitleLabel {
                font-size: 16px; 
                font-weight: normal;
                color: #555555;
                padding-top: 0px;
                margin-top: 0px; /* Pulls it slightly closer to the main title */
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #000000;
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: #f8f8f8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                padding: 12px 20px;
                font-weight: bold;
                border-radius: 6px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit {
                border: 2px solid #000000;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: #ffffff;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #444444;
            }
            QTextEdit {
                border: 2px solid #000000;
                border-radius: 4px;
                padding: 8px;
                background-color: #fafafa;
                color: #000000;
                font-family: 'Courier New', monospace;
                font-size: 20px;
            }
            QMenuBar {
                background-color: #000000;
                color: #ffffff;
                font-weight: bold;
                border-bottom: 2px solid #333333;
            }
            QMenuBar::item {
                spacing: 3px;
                padding: 8px 15px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #333333;
                border-radius: 4px;
            }
            QProgressDialog{
            background-color: white;
            }
            QMenu {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                background: transparent;
            }
            QMenu::item:selected {
                background-color: #000000;
                color: #ffffff;
            }
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                margin: 5px;
            }
        """)


# NOTE:  to build this into .exe run
# uv run pyinstaller --name=app --add-data "src/desctop_app/languages:languages" src/desctop_app/app.py
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # PyInstaller creates a temporary folder and stores path in _MEIPASS
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        BASE_DIR = Path(sys._MEIPASS)
    elif "__file__" in locals():
        BASE_DIR = Path(__file__).resolve().parent
    else:
        BASE_DIR = Path.cwd()

    LANG_DIR = BASE_DIR / "languages"

    # Check if the uk.json exists, otherwise fallback gracefully or handle error
    initial_lang_path = LANG_DIR / "uk.json"

    tr = UILanguageManager(str(initial_lang_path))

    window = MainWindow(tr, LANG_DIR)
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
