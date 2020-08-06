from PySide2 import QtCore
from PySide2.QtGui import QFont, QStandardItemModel, QMovie, QStandardItem
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QStackedWidget, QTableView, QAbstractItemView, \
    QHeaderView, QWidget


class CurrentStateWindow:

    def __init__(self, gui, state_manager):
        self.lower_box = QGroupBox()
        self._lower_parent_layout = QVBoxLayout()
        self._lower_stacked_widget = QStackedWidget()
        self._state_manager = state_manager
        self._underline_font = None
        self.gui = gui
        self._current_window_stacked_widget = QStackedWidget()
        self._is_first = True
        self._current_parent_widget = QWidget()
        self._coils_table_view = QTableView()
        self._coils_table_rows = QStandardItemModel()
        self._d_inputs_parent_widget = QWidget()
        self._d_inputs_table_view = QTableView()
        self._d_inputs_table_rows = QStandardItemModel()
        self._h_reg_parent_widget = QWidget()
        self._h_reg_table_view = QTableView()
        self._h_reg_table_rows = QStandardItemModel()
        self._i_reg_parent_widget = QWidget()
        self._i_reg_table_view = QTableView()
        self._i_reg_table_rows = QStandardItemModel()
        self._coils_wr_parent_widget = QWidget()
        self._coils_wr_table_view = QTableView()
        self._coils_wr_table_rows = QStandardItemModel()
        self._wr_i_reg_parent_widget = QWidget()
        self._wr_i_reg_table_view = QTableView()
        self._wr_i_reg_table_rows = QStandardItemModel()

    def init_current_state_window(self):
        self._underline_font = QFont("Arial", 12)
        self._underline_font.setUnderline(True)
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
        self._lower_stacked_widget.addWidget(loading_parent_widget)

        self._set_current_coils()
        self._lower_stacked_widget.addWidget(self._current_parent_widget)
        self._set_current_discrete_inputs()
        self._lower_stacked_widget.addWidget(self._d_inputs_parent_widget)
        self._set_current_holding_registers()
        self._lower_stacked_widget.addWidget(self._h_reg_parent_widget)
        self._set_current_input_registers()
        self._lower_stacked_widget.addWidget(self._i_reg_parent_widget)
        self._set_current_coils_write()
        self._lower_stacked_widget.addWidget(self._coils_wr_parent_widget)
        self._set_current_input_registers_write()
        self._lower_stacked_widget.addWidget(self._wr_i_reg_parent_widget)

        self._lower_parent_layout.addWidget(self._lower_stacked_widget)
        self.lower_box.setLayout(self._lower_parent_layout)
        self.gui._lower_box = self.lower_box

    def signal_current_state_window_from_gui(self):
        if self._is_first is False:
            current_function = self.gui.left_side_select_operation_box.currentIndex() + 1
            self._lower_stacked_widget.setCurrentIndex(current_function)
            current_function = str(hex(current_function))[2:].rjust(2, '0')
            self._update_table(current_function)

    def signal_current_state_window_from_state_manager(self, is_first):
        if self._is_first is True:
            self._is_first = is_first
            self.signal_current_state_window_from_gui()
        current_function = self._state_manager.live_update_states["currently_selected_function"]
        self._update_table(current_function)

    def _update_table(self, current_function):
        if current_function == "01":
            self._update_current_coils()
        elif current_function == "02":
            self._update_current_discrete_inputs()
        elif current_function == "03":
            self._update_current_holding_registers()
        elif current_function == "04":
            self._update_current_input_registers()
        elif current_function == "05":
            self._update_current_coils_write()
        elif current_function == "06":
            self._update_current_input_registers_write()

    def _set_current_coils(self):
        coils_parent_layout = QVBoxLayout()
        coils_label = QLabel("Current state in the coils:")
        coils_label.setFont(self._underline_font)
        coils_parent_layout.addWidget(coils_label)
        self._coils_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._coils_table_view.horizontalHeader().setStretchLastSection(True)
        self._coils_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._coils_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])
        self._coils_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_coils()
        coils_parent_layout.addWidget(self._coils_table_view)
        self._current_parent_widget.setLayout(coils_parent_layout)

    def _update_current_coils(self):
        self._update_current_coils_write()
        self._coils_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])
        self._coils_table_rows.removeRows(0, self._coils_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_coils"]["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_table_rows.appendRow([error])
            return
        current_coils_dict = self._state_manager.live_update_states["current_read_coils"]
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
            self._coils_table_rows.appendRow([current_unit_address, current_address, current_coil_value])
        self._coils_table_view.setModel(self._coils_table_rows)

    def _set_current_discrete_inputs(self):
        discrete_inputs_parent_layout = QVBoxLayout()
        discrete_inputs_label = QLabel("Current state in the discrete inputs:")
        discrete_inputs_label.setFont(self._underline_font)
        discrete_inputs_parent_layout.addWidget(discrete_inputs_label)
        self._d_inputs_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._d_inputs_table_view.horizontalHeader().setStretchLastSection(True)
        self._d_inputs_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._d_inputs_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "DISCRETE INPUT ADDRESS", "VALUE"])
        self._d_inputs_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_discrete_inputs()
        discrete_inputs_parent_layout.addWidget(self._d_inputs_table_view)
        self._d_inputs_parent_widget.setLayout(discrete_inputs_parent_layout)

    def _update_current_discrete_inputs(self):
        self._d_inputs_table_rows.removeRows(0, self._d_inputs_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_discrete_inputs"]
        err = err["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_table_rows.appendRow([error])
            return
        current_discrete_inputs_dict = self._state_manager.live_update_states["current_read_discrete_inputs"]
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
            self._d_inputs_table_rows.appendRow([current_unit_address, current_address, current_discrete_inputs_value])
        self._d_inputs_table_view.setModel(self._d_inputs_table_rows)

    def _set_current_holding_registers(self):
        holding_registers_parent_layout = QVBoxLayout()
        holding_registers_label = QLabel("Current state in the holding registers:")
        holding_registers_label.setFont(self._underline_font)
        holding_registers_parent_layout.addWidget(holding_registers_label)
        self._h_reg_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._h_reg_table_view.horizontalHeader().setStretchLastSection(True)
        self._h_reg_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._h_reg_table_rows.setHorizontalHeaderLabels(
            ["UNIT ADDRESS", "HOLDING REGISTER ADDRESS", "VALUE"])
        self._h_reg_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_holding_registers()
        holding_registers_parent_layout.addWidget(self._h_reg_table_view)
        self._h_reg_parent_widget.setLayout(holding_registers_parent_layout)

    def _update_current_holding_registers(self):
        self._h_reg_table_rows.removeRows(0, self._h_reg_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_holding_registers"]
        err = err["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_table_rows.appendRow([error])
            return
        current_holding_registers_dict = self._state_manager.live_update_states["current_read_holding_registers"]
        unit_address = current_holding_registers_dict["current_unit_address"]
        start_address = hex(current_holding_registers_dict["current_request_from_gui"][0])
        no_of_holding_registers = current_holding_registers_dict["current_request_from_gui"][1]
        holding_registers = current_holding_registers_dict["current_response_returned_values"]
        start_address = int(start_address, 16)
        active_holding_registers = {}
        for returned_value in holding_registers:
            adr = returned_value[0]
            if adr != "-":
                val = returned_value[1]
                active_holding_registers[adr] = val
        for i in range(0, no_of_holding_registers):
            current_holding_registers_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_holding_registers.keys():
                current_holding_registers_value = active_holding_registers[current_address]
            current_holding_registers_value = QStandardItem(str(current_holding_registers_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            self._h_reg_table_rows.appendRow([current_unit_address, current_address, current_holding_registers_value])
        self._h_reg_table_view.setModel(self._h_reg_table_rows)

    def _set_current_input_registers(self):
        input_registers_parent_layout = QVBoxLayout()
        input_registers_label = QLabel("Current state in the input registers:")
        input_registers_label.setFont(self._underline_font)
        input_registers_parent_layout.addWidget(input_registers_label)
        self._i_reg_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._i_reg_table_view.horizontalHeader().setStretchLastSection(True)
        self._i_reg_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._i_reg_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "INPUT REGISTER ADDRESS", "VALUE"])
        self._i_reg_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_input_registers()
        input_registers_parent_layout.addWidget(self._i_reg_table_view)
        self._i_reg_parent_widget.setLayout(input_registers_parent_layout)

    def _update_current_input_registers(self):
        self._i_reg_table_rows.removeRows(0, self._i_reg_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_input_registers"]
        err = err["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_table_rows.appendRow([error])
            return
        current_input_registers_dict = self._state_manager.live_update_states["current_read_input_registers"]
        unit_address = current_input_registers_dict["current_unit_address"]
        start_address = hex(current_input_registers_dict["current_request_from_gui"][0])
        no_of_input_registers = current_input_registers_dict["current_request_from_gui"][1]
        returned_values = current_input_registers_dict["current_response_returned_values"]
        active_input_registers = {}
        for returned_value in returned_values:
            adr = returned_value[0]
            if adr != "-":
                val = returned_value[1]
                active_input_registers[adr] = val
        start_address = int(start_address, 16)
        for i in range(0, no_of_input_registers):
            current_input_registers_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_input_registers.keys():
                current_input_registers_value = active_input_registers[current_address]
            current_input_registers_value = QStandardItem(str(current_input_registers_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            self._i_reg_table_rows.appendRow([current_unit_address, current_address, current_input_registers_value])
        self._i_reg_table_view.setModel(self._i_reg_table_rows)

    def _set_current_coils_write(self):
        coils_write_parent_layout = QVBoxLayout()
        coils_write_label = QLabel("Current state in the coils:")
        coils_write_label.setFont(self._underline_font)
        coils_write_parent_layout.addWidget(coils_write_label)
        self._coils_wr_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._coils_wr_table_view.horizontalHeader().setStretchLastSection(True)
        self._coils_wr_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._coils_wr_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])
        self._coils_wr_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_coils_write()
        coils_write_parent_layout.addWidget(self._coils_wr_table_view)
        self._coils_wr_parent_widget.setLayout(coils_write_parent_layout)

    def _update_current_coils_write(self):
        self._coils_wr_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "COIL ADDRESS", "VALUE"])
        self._coils_wr_table_rows.removeRows(0, self._coils_wr_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_coils"]["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_wr_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_wr_table_rows.appendRow([error])
            return
        current_coils_write_dict = self._state_manager.live_update_states["current_read_coils"]
        unit_address = current_coils_write_dict["current_unit_address"]
        start_address = hex(current_coils_write_dict["current_request_from_gui"][0])
        no_of_coils = current_coils_write_dict["current_request_from_gui"][1]
        active_coils = current_coils_write_dict["current_response_returned_values"]
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
            self._coils_wr_table_rows.appendRow([current_unit_address, current_address, current_coil_value])
        self._coils_wr_table_view.setModel(self._coils_wr_table_rows)

    def _set_current_input_registers_write(self):
        write_input_registers_parent_layout = QVBoxLayout()
        write_input_registers_label = QLabel("Current state in the input registers:")
        write_input_registers_label.setFont(self._underline_font)
        write_input_registers_parent_layout.addWidget(write_input_registers_label)
        self._wr_i_reg_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._wr_i_reg_table_view.horizontalHeader().setStretchLastSection(True)
        self._wr_i_reg_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._wr_i_reg_table_rows.setHorizontalHeaderLabels(["UNIT ADDRESS", "INPUT REGISTER ADDRESS", "VALUE"])
        self._wr_i_reg_table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._update_current_input_registers_write()
        write_input_registers_parent_layout.addWidget(self._wr_i_reg_table_view)
        self._wr_i_reg_parent_widget.setLayout(write_input_registers_parent_layout)

    def _update_current_input_registers_write(self):
        self._wr_i_reg_table_rows.removeRows(0, self._wr_i_reg_table_rows.rowCount())
        err = self._state_manager.live_update_states["current_read_input_registers"]
        err = err["current_response_err_msg"]
        if err != "-" and len(err) != 0:
            self._coils_table_rows.setHorizontalHeaderLabels(["ERROR", "", ""])
            error = QStandardItem(str(err))
            self._coils_table_rows.appendRow([error])
            return
        current_write_input_registers_dict = \
            self._state_manager.live_update_states["current_read_input_registers"]
        unit_address = current_write_input_registers_dict["current_unit_address"]
        start_address = hex(current_write_input_registers_dict["current_request_from_gui"][0])
        no_of_write_input_registers = current_write_input_registers_dict["current_request_from_gui"][1]
        returned_values = current_write_input_registers_dict["current_response_returned_values"]
        active_write_input_registers = {}
        for returned_value in returned_values:
            adr = returned_value[0]
            if adr != "-":
                val = returned_value[1]
                active_write_input_registers[adr] = val
        start_address = int(start_address, 16)
        for i in range(0, no_of_write_input_registers):
            current_write_input_reg_value = 0
            current_address = hex(start_address + i)
            current_unit_address = unit_address
            if current_address in active_write_input_registers.keys():
                current_write_input_reg_value = active_write_input_registers[current_address]
            current_write_input_reg_value = QStandardItem(str(current_write_input_reg_value))
            current_address = QStandardItem(str(current_address))
            current_unit_address = QStandardItem(str(current_unit_address))
            self._wr_i_reg_table_rows.appendRow([current_unit_address, current_address, current_write_input_reg_value])
        self._wr_i_reg_table_view.setModel(self._wr_i_reg_table_rows)
