from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import  QFont

class PageOne(QtWidgets.QWidget):
    def __init__(self, tr):
        super().__init__()
        self.tr = tr
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)

        self.label = QtWidgets.QLabel(
            self.tr.get("documentation_page.title"), alignment=QtCore.Qt.AlignCenter
        )
        self.label.setFont(QFont("Arial", 20, QFont.Bold))

        self.content = QtWidgets.QLabel(
            self.tr.get("documentation_page.content"),
            alignment=QtCore.Qt.AlignLeft,
        )
        self.content.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.content)
        self.layout.addStretch()

    def refresh_ui(self):
        self.label.setText(self.tr.get("documentation_page.title"))
        self.content.setText(
            self.tr.get("documentation_page.content").replace("\\n", "\n")
        )
