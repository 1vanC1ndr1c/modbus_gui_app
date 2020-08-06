from PySide2 import QtCore
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout


def _init_error_window(message):
    error_dlg_window = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
    error_dlg_window.setWindowTitle("ERROR")
    error_font = QFont("Arial", 12)
    error_label = QLabel(message)
    error_label.setStyleSheet("color: red")
    error_label.setFont(error_font)
    error_layout = QVBoxLayout()
    error_layout.addWidget(error_label)
    error_dlg_window.setLayout(error_layout)
    error_dlg_window.exec_()
