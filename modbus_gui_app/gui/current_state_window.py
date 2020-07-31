from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QStackedWidget, QTableView, QAbstractItemView, \
    QHeaderView, QWidget
from PySide2.QtGui import QFont, QStandardItemModel, QMovie, QStandardItem
from PySide2 import QtCore


class CurrentStateWindow:

    def __init__(self, gui, state_manager):
        self.lower_box = QGroupBox()
        self.lower_parent_layout = QVBoxLayout()
        self.lower_stacked_widget = QStackedWidget()
        self.state_manager = state_manager
        self.underline_font = None
        self.gui = gui
        self.current_window_stacked_widget = QStackedWidget()
        self.is_first = True
        self.current_coils_parent_widget = QWidget()
        self.coils_table_view = QTableView()
        self.coils_table_rows = QStandardItemModel()
        self.current_discrete_inputs_parent_widget = QWidget()
        self.discrete_inputs_table_view = QTableView()
        self.discrete_inputs_table_rows = QStandardItemModel()
        self.current_holding_registers_parent_widget = QWidget()
        self.holding_registers_table_view = QTableView()
        self.holding_registers_table_rows = QStandardItemModel()

    def init_current_state_window(self):
        self.underline_font = QFont("Arial", 12)
        self.underline_font.setUnderline(True)
        self.lower_box.setMinimumHeight(400)
        self.lower_box.setStyleSheet("background-color: white")

        loading_parent_widget = QWidget()
        loading_layout = QVBoxLayout()
        loading_label = QLabel()
        loading_layout.setAlignment(QtCore.Qt.AlignTop)
        loading_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_gif = QMovie("resources/loading.gif")
        loading_label.setMovie(loading_gif)
        loading_gif.start()
        loading_layout.addWidget(loading_label)
        loading_parent_widget.setLayout(loading_layout)
        self.lower_stacked_widget.addWidget(loading_parent_widget)

        self.set_coils_current_state()
        self.lower_stacked_widget.addWidget(self.current_coils_parent_widget)

        self.set_discrete_inputs_current_state()
        self.lower_stacked_widget.addWidget(self.current_discrete_inputs_parent_widget)

        self.set_holding_registers_current_state()
        self.lower_stacked_widget.addWidget(self.current_holding_registers_parent_widget)

        ph4 = QLabel("PLACEHOLDER4")
        self.lower_stacked_widget.addWidget(ph4)
        ph5 = QLabel("PLACEHOLDER5")
        self.lower_stacked_widget.addWidget(ph5)

        self.lower_parent_layout.addWidget(self.lower_stacked_widget)
        self.lower_box.setLayout(self.lower_parent_layout)
        self.gui.lower_box = self.lower_box

    def signal_current_state_window_from_gui(self):
        if self.is_first is False:
            current_function = self.gui.left_side_select_operation_box.currentIndex() + 1
            self.lower_stacked_widget.setCurrentIndex(current_function)
            current_function = str(hex(current_function))[2:].rjust(2, '0')
            self.update_table(current_function)

    def signal_current_state_window_from_state_manager(self, is_first):
        if self.is_first is True:
            self.is_first = is_first
            self.signal_current_state_window_from_gui()

        current_function = self.state_manager.current_coil_input_reg_states["currently_selected_function"]
        self.update_table(current_function)

    def update_table(self, current_function):
        if current_function == "01":
            self.update_coils_current_state()
        elif current_function == "02":
            self.update_discrete_inputs_current_state()
        elif current_function == "03":
            self.update_holding_registers_current_state()

    def set_coils_current_state(self):
        coils_parent_layout = QVBoxLayout()

        coils_label = QLabel("Current state in the coils:")
        coils_label.setFont(self.underline_font)
        coils_parent_layout.addWidget(coils_label)

        self.coils_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.coils_table_view.horizontalHeader().setStretchLastSection(True)
        self.coils_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.coils_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])
        self.coils_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")

        self.update_coils_current_state()

        coils_parent_layout.addWidget(self.coils_table_view)
        self.current_coils_parent_widget.setLayout(coils_parent_layout)

    def update_coils_current_state(self):

        self.coils_table_rows.removeRows(0, self.coils_table_rows.rowCount())
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
            self.coils_table_rows.appendRow([current_unit_address, current_address, current_coil_value])
        self.coils_table_view.setModel(self.coils_table_rows)

    def set_discrete_inputs_current_state(self):
        discrete_inputs_parent_layout = QVBoxLayout()

        discrete_inputs_label = QLabel("Current state in the discrete inputs:")
        discrete_inputs_label.setFont(self.underline_font)
        discrete_inputs_parent_layout.addWidget(discrete_inputs_label)

        self.discrete_inputs_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.discrete_inputs_table_view.horizontalHeader().setStretchLastSection(True)
        self.discrete_inputs_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.discrete_inputs_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "DISCRETE INPUT ADDRESS", "VALUE"])
        self.discrete_inputs_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")

        self.update_discrete_inputs_current_state()

        discrete_inputs_parent_layout.addWidget(self.discrete_inputs_table_view)
        self.current_discrete_inputs_parent_widget.setLayout(discrete_inputs_parent_layout)

    def update_discrete_inputs_current_state(self):

        self.discrete_inputs_table_rows.removeRows(0, self.discrete_inputs_table_rows.rowCount())

        current_discrete_inputs_dict = \
            self.state_manager.current_coil_input_reg_states["current_read_discrete_inputs"]

        unit_address = current_discrete_inputs_dict["current_unit_address"]
        start_address = hex(current_discrete_inputs_dict["current_request_from_gui"][0])
        no_of_discrete_inputs = current_discrete_inputs_dict["current_request_from_gui"][1]
        active_discrete_inputs = current_discrete_inputs_dict["current_response_returned_values"]

        start_address = int(start_address, 16)
        for i in range(0, no_of_discrete_inputs):
            current_discrete_inputs_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_discrete_inputs:
                current_discrete_inputs_value = 1
            current_discrete_inputs_value = QStandardItem(str(current_discrete_inputs_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            self.discrete_inputs_table_rows.appendRow(
                [current_unit_address, current_address, current_discrete_inputs_value])
        self.discrete_inputs_table_view.setModel(self.discrete_inputs_table_rows)

    def set_holding_registers_current_state(self):
        holding_registers_parent_layout = QVBoxLayout()

        holding_registers_label = QLabel("Current state in the holding registers:")
        holding_registers_label.setFont(self.underline_font)
        holding_registers_parent_layout.addWidget(holding_registers_label)

        self.holding_registers_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.holding_registers_table_view.horizontalHeader().setStretchLastSection(True)
        self.holding_registers_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.holding_registers_table_rows.setHorizontalHeaderLabels(
            ["UNIT ADDRESS", "HOLDING REGISTER ADDRESS", "VALUE"])
        self.holding_registers_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")

        self.update_holding_registers_current_state()

        holding_registers_parent_layout.addWidget(self.holding_registers_table_view)
        self.current_holding_registers_parent_widget.setLayout(holding_registers_parent_layout)

    def update_holding_registers_current_state(self):

        self.holding_registers_table_rows.removeRows(0, self.holding_registers_table_rows.rowCount())

        current_holding_registers_dict = \
            self.state_manager.current_coil_input_reg_states["current_read_holding_registers"]

        unit_address = current_holding_registers_dict["current_unit_address"]
        start_address = hex(current_holding_registers_dict["current_request_from_gui"][0])
        no_of_holding_registers = current_holding_registers_dict["current_request_from_gui"][1]
        active_holding_registers = current_holding_registers_dict["current_response_returned_values"]

        start_address = int(start_address, 16)
        for i in range(0, no_of_holding_registers):
            current_holding_registers_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_holding_registers:
                current_holding_registers_value = 1
            current_holding_registers_value = QStandardItem(str(current_holding_registers_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            self.holding_registers_table_rows.appendRow(
                [current_unit_address, current_address, current_holding_registers_value])
        self.holding_registers_table_view.setModel(self.holding_registers_table_rows)
