import sys

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QPushButton

from logic.request_processing import process_request


def init_gui():
    app = QApplication(sys.argv)
    app.setApplicationName("MODBUS")
    window = QWidget()
    font = QFont("Arial", 12)
    window.setFont(font)
    layout = QVBoxLayout()

    label_choose_operation = QLabel("Choose an operation:")
    layout.addWidget(label_choose_operation)

    combo_box = QComboBox()
    combo_box.addItem("default")
    combo_box.addItem("not impl1")
    combo_box.addItem("not impl2")
    combo_box.addItem("not impl3")
    combo_box.addItem("not impl4")
    layout.addWidget(combo_box)

    button_submit = QPushButton("Submit")
    button_submit.setStyleSheet("background-color: green")
    button_submit.setFont(font)
    layout.addWidget(button_submit)
    #TODO pass arguments into this function
    button_submit.clicked.connect(process_request)

    window.setLayout(layout)
    window.show()
    app.exec_()