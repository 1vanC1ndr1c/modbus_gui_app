from PySide2.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton
from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore


def init_history_window(db_read_queue):
    history_dlg_window = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
    history_dlg_window.setMinimumWidth(1025)
    history_dlg_window.setMinimumHeight(500)
    history_dlg_window.setWindowTitle("HISTORY")
    history_parent_layout = QVBoxLayout()

    # table
    table_widget = QTableView()
    names = QStandardItemModel()
    names.setHorizontalHeaderLabels(["TIME STAMP", "TRANSACTION ID", "TYPE", "PROTOCOL",
                                     "LENGTH", "UNIT_ADDRESS", "FUNCTION CODE", "MODBUS DATA"])
    table_widget.setStyleSheet("QHeaderView::section { background-color:lightgray }")
    table_widget.setModel(names)
    history_parent_layout.addWidget(table_widget)

    # Submit buttton and it's functionality
    button_submit = QPushButton()
    button_submit.setText("Get Data")
    button_submit.setStyleSheet("background-color: green")
    button_submit.sizeHint()
    history_parent_layout.addWidget(button_submit)

    data = []
    # button_submit.clicked.connect(
    #     lambda c: db_read(10, data))
    history_dlg_window.setLayout(history_parent_layout)
    history_dlg_window.exec_()
