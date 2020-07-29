from PySide2 import QtCore
from PySide2.QtGui import QFont, QStandardItemModel
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QPushButton, QScrollArea, QStackedWidget, QTableView, QAbstractItemView, QHeaderView

from modbus_gui_app.logic.validation import validate_current_state_data
from modbus_gui_app.gui.error_window import init_error_window


class CurrentStateWindow:

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.underline_font = None

    def init_current_state_window(self, font, left_side_select_operation_box):
        lower_box = QGroupBox()
        lower_box.setMinimumHeight(400)
        parent_layout = QVBoxLayout()
        parent_layout.setAlignment(QtCore.Qt.AlignTop)
        self.underline_font = QFont("Arial", 12)
        self.underline_font.setUnderline(True)

        current_state_stacked_widget = QStackedWidget()
        coils_current_state = self.set_coils_current_state()
        second_state = QLabel("Second")
        third_state = QLabel("Third")
        current_state_stacked_widget.addWidget(coils_current_state)
        current_state_stacked_widget.addWidget(second_state)
        current_state_stacked_widget.addWidget(third_state)
        left_side_select_operation_box.activated[int].connect(current_state_stacked_widget.setCurrentIndex)

        parent_layout.addWidget(current_state_stacked_widget)
        lower_box.setLayout(parent_layout)

        return lower_box

    def set_coils_current_state(self):
        coils_parent_widget = QLabel()
        coils_parent_layout = QVBoxLayout()

        coils_label = QLabel("Current state in coils:")
        coils_label.setFont(self.underline_font)
        coils_parent_layout.addWidget(coils_label)

        coils_table_view = QTableView()
        coils_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        coils_table_view.horizontalHeader().setStretchLastSection(True)
        coils_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        coils_table_rows = QStandardItemModel()
        coils_table_rows.setHorizontalHeaderLabels(["ADDRESS",
                                                    "VALUE",
                                                    "TIME OF THE LAST CHANGE"])

        coils_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        coils_table_view.setModel(coils_table_rows)
        coils_parent_layout.addWidget(coils_table_view)

        coils_parent_widget.setLayout(coils_parent_layout)

        return coils_parent_widget
