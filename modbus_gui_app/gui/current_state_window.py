from PySide2 import QtCore
from PySide2.QtGui import QFont, QStandardItemModel, QMovie, QStandardItem
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QPushButton, QScrollArea, QStackedWidget, QTableView, QAbstractItemView, QHeaderView

from modbus_gui_app.logic.validation import validate_current_state_data
from modbus_gui_app.gui.gui_middle import reset_layout
from modbus_gui_app.gui.error_window import init_error_window


class CurrentStateWindow:

    def __init__(self, gui, state_manager):
        self.state_manager = state_manager
        self.underline_font = None
        self.gui = gui

    def init_current_state_window(self, font, left_side_select_operation_box, lower_box, is_first):
        self.underline_font = QFont("Arial", 12)
        self.underline_font.setUnderline(True)
        self.gui.lower_box.setMinimumHeight(400)

        if is_first is True:
            self.gui.lower_box = QGroupBox()
            loading_layout = QVBoxLayout()
            self.gui.lower_box.setStyleSheet("background-color: white")
            loading_layout.setAlignment(QtCore.Qt.AlignTop)
            loading_label = QLabel()
            loading_label.setAlignment(QtCore.Qt.AlignCenter)
            loading_gif = QMovie("resources/loading.gif")
            loading_label.setMovie(loading_gif)
            loading_gif.start()
            loading_layout.addWidget(loading_label)
            self.gui.lower_box.setLayout(loading_layout)

        if is_first is False:
            self.gui.lower_box.deleteLater()
            self.gui.lower_box = QGroupBox()
            parent_layout = QVBoxLayout()
            parent_layout.setAlignment(QtCore.Qt.AlignTop)
            self.gui.lower_box.setLayout(parent_layout)
            self.gui.parent_layout.addWidget(self.gui.lower_box)

            current_index = self.gui.left_side_select_operation_box.currentIndex() + 1
            current_operation = self.state_manager.current_coil_input_reg_states["currently_selected_function"]
            # TODO 4 and up is wrongly calculated
            # print(current_index, current_operation)
            if current_index == 1:
                coils_parent_widget = self.set_coils_current_state()
                parent_layout.addWidget(coils_parent_widget)
            else:
                parent_layout.addWidget(QLabel("NO"))

            self.gui.lower_box.setLayout(parent_layout)
            self.gui.parent_layout.addWidget(self.gui.lower_box)

    def set_coils_current_state(self):
        coils_parent_widget = QLabel()
        coils_parent_layout = QVBoxLayout()

        coils_label = QLabel("Current state in the coils:")
        coils_label.setFont(self.underline_font)
        coils_parent_layout.addWidget(coils_label)

        coils_table_view = QTableView()
        coils_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        coils_table_view.horizontalHeader().setStretchLastSection(True)
        coils_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        coils_table_rows = QStandardItemModel()
        coils_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])

        coils_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        coils_table_view.setModel(coils_table_rows)
        coils_parent_layout.addWidget(coils_table_view)

        current_coils_dict = self.state_manager.current_coil_input_reg_states["current_read_coils"]
        unit_address = current_coils_dict["current_unit_address"]
        start_address = hex(current_coils_dict["current_request_from_gui"][0])
        no_of_coils = current_coils_dict["current_request_from_gui"][1]
        active_coils = current_coils_dict["current_response_returned_values"]

        start_address = int(start_address, 16)
        for i in range(0, no_of_coils):
            current_coil_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_coils:
                current_coil_value = 1
            current_coil_value = QStandardItem(str(current_coil_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            coils_table_rows.appendRow([current_unit_address, current_address, current_coil_value])

        coils_parent_widget.setLayout(coils_parent_layout)
        return coils_parent_widget
