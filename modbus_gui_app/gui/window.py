import sys

from PySide2 import QtCore
from PySide2.QtGui import QFont, QStandardItemModel
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QPushButton, QStackedWidget, \
    QHBoxLayout, QLineEdit, QDialog, QSizePolicy, QFrame, QScrollArea, QMenu, QMainWindow, QAction, QTableView

from  modbus_gui_app.logic import validation
from modbus_gui_app.database import db_read
from modbus_gui_app.logic.response_processing import process_response, get_response


def init_gui(request_queue, response_queue, db_write_queue, db_read_queue):
    app = QApplication(sys.argv)
    app.setApplicationName("MODBUS")
    window = QMainWindow()
    window.setGeometry(300, 300, 1200, 450)
    main_widget = QWidget()
    font = QFont("Arial", 12)
    main_widget.setFont(font)
    parent_layout = QHBoxLayout()
    right_side_layout = QVBoxLayout()
    left_side_layout = QVBoxLayout()

    menu_bar = window.menuBar()
    menu = QMenu("History")
    history_action = QAction("Open History")
    history_action.setShortcut("Ctrl+H")
    history_action.setStatusTip("See the history of requests and responses")
    history_action.triggered.connect(lambda l: init_history_window(db_read_queue))
    menu.addAction(history_action)
    menu_bar.addMenu(menu)

    # Left side of the window =========================================================================================
    select_operation_layout = QHBoxLayout()
    select_operation_label = QLabel("Select an operation:")
    select_operation_layout.addWidget(select_operation_label)
    select_operation_combo_box = QComboBox()
    select_operation_combo_box.addItem("Read Coils")
    select_operation_combo_box.addItem("Read Discrete Inputs")
    select_operation_combo_box.addItem("Read Holding Registers")
    select_operation_combo_box.addItem("Read Input Registers")
    select_operation_combo_box.addItem("Write Single Coil")
    select_operation_combo_box.addItem("Write Single Register")
    select_operation_combo_box.addItem("not impl6")
    select_operation_combo_box.addItem("not impl7")
    select_operation_combo_box.addItem("not impl8")
    select_operation_layout.addWidget(select_operation_combo_box)
    left_side_layout.addLayout(select_operation_layout)

    # Create additional options based on the selected options in the drop down menu.
    additional_options_stacked_widget = QStackedWidget()

    # Read Coils.
    read_coils_option_parent_widget = QWidget()
    read_coils_option_parent_layout = QVBoxLayout()
    read_coils_option_first_row_layout = QHBoxLayout()
    read_coils_option_first_row_text = QLabel("Starting Address(hex):")
    read_coils_option_first_row_input = QLineEdit()
    read_coils_option_first_row_input.setPlaceholderText("Insert the starting address...")
    read_coils_option_first_row_input.setMinimumWidth(300)
    read_coils_option_first_row_layout.addWidget(read_coils_option_first_row_text)
    read_coils_option_first_row_layout.addWidget(read_coils_option_first_row_input)
    read_coils_option_parent_layout.addLayout(read_coils_option_first_row_layout)
    read_coils_option_second_row_layout = QHBoxLayout()
    read_coils_option_second_row_text = QLabel("Number of coils(dec):")
    read_coils_option_second_row_input = QLineEdit()
    read_coils_option_second_row_input.setPlaceholderText("Insert the number of coils...")
    read_coils_option_second_row_layout.addWidget(read_coils_option_second_row_text)
    read_coils_option_second_row_layout.addWidget(read_coils_option_second_row_input)
    read_coils_option_parent_layout.addLayout(read_coils_option_second_row_layout)
    read_coils_option_third__row_layout = QHBoxLayout()
    read_coils_option_third__row_text = QLabel("Unit Address(dec):")
    read_coils_option_third__row_input = QLineEdit()
    read_coils_option_third__row_input.setPlaceholderText("Insert the unit address...")
    read_coils_option_third__row_layout.addWidget(read_coils_option_third__row_text)
    read_coils_option_third__row_layout.addWidget(read_coils_option_third__row_input)
    read_coils_option_parent_layout.addLayout(read_coils_option_third__row_layout)
    read_coils_option_parent_widget.setLayout(read_coils_option_parent_layout)
    additional_options_stacked_widget.addWidget(read_coils_option_parent_widget)

    # Read Discrete Inputs.
    read_discrete_inputs_option_parent_widget = QWidget()
    read_discrete_inputs_option_parent_layout = QVBoxLayout()
    read_discrete_inputs_option_first_row_layout = QHBoxLayout()
    read_discrete_inputs_option_first_row_text = QLabel("First input address(hex):")
    read_discrete_inputs_option_first_row_input = QLineEdit()
    read_discrete_inputs_option_first_row_input.setPlaceholderText("Insert the first input address...")
    read_discrete_inputs_option_first_row_input.setMinimumWidth(300)
    read_discrete_inputs_option_first_row_layout.addWidget(read_discrete_inputs_option_first_row_text)
    read_discrete_inputs_option_first_row_layout.addWidget(read_discrete_inputs_option_first_row_input)
    read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_first_row_layout)
    read_discrete_inputs_option_second_row_layout = QHBoxLayout()
    read_discrete_inputs_option_second_row_text = QLabel("Register count(dec):")
    read_discrete_inputs_option_second_row_input = QLineEdit()
    read_discrete_inputs_option_second_row_input.setPlaceholderText("Insert the number of registers...")
    read_discrete_inputs_option_second_row_layout.addWidget(read_discrete_inputs_option_second_row_text)
    read_discrete_inputs_option_second_row_layout.addWidget(read_discrete_inputs_option_second_row_input)
    read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_second_row_layout)
    read_discrete_inputs_option_third_row_layout = QHBoxLayout()
    read_discrete_inputs_option_third_row_text = QLabel("Unit Address(dec):")
    read_discrete_inputs_option_third_row_input = QLineEdit()
    read_discrete_inputs_option_third_row_input.setPlaceholderText("Insert the unit address...")
    read_discrete_inputs_option_third_row_layout.addWidget(read_discrete_inputs_option_third_row_text)
    read_discrete_inputs_option_third_row_layout.addWidget(read_discrete_inputs_option_third_row_input)
    read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_third_row_layout)
    read_discrete_inputs_option_parent_widget.setLayout(read_discrete_inputs_option_parent_layout)
    additional_options_stacked_widget.addWidget(read_discrete_inputs_option_parent_widget)

    # Read Holding Registers.
    read_holding_registers_option_parent_widget = QWidget()
    read_holding_registers_option_parent_layout = QVBoxLayout()
    read_holding_registers_option_first_row_layout = QHBoxLayout()
    read_holding_registers_option_first_row_text = QLabel("First input address(hex):")
    read_holding_registers_option_first_row_input = QLineEdit()
    read_holding_registers_option_first_row_input.setPlaceholderText("Insert the first input address...")
    read_holding_registers_option_first_row_input.setMinimumWidth(300)
    read_holding_registers_option_first_row_layout.addWidget(read_holding_registers_option_first_row_text)
    read_holding_registers_option_first_row_layout.addWidget(read_holding_registers_option_first_row_input)
    read_holding_registers_option_parent_layout.addLayout(read_holding_registers_option_first_row_layout)
    read_holding_registers_option_second_row_layout = QHBoxLayout()
    read_holding_registers_option_second_row_text = QLabel("Register count(dec):")
    read_holding_registers_option_second_row_input = QLineEdit()
    read_holding_registers_option_second_row_input.setPlaceholderText("Insert the number of registers...")
    read_holding_registers_option_second_row_layout.addWidget(read_holding_registers_option_second_row_text)
    read_holding_registers_option_second_row_layout.addWidget(read_holding_registers_option_second_row_input)
    read_holding_registers_option_parent_layout.addLayout(read_holding_registers_option_second_row_layout)
    read_holding_registers_option_third_row_layout = QHBoxLayout()
    read_holding_registers_option_third_row_text = QLabel("Unit Address(dec):")
    read_holding_registers_option_third_row_input = QLineEdit()
    read_holding_registers_option_third_row_input.setPlaceholderText("Insert the unit address...")
    read_holding_registers_option_third_row_layout.addWidget(read_holding_registers_option_third_row_text)
    read_holding_registers_option_third_row_layout.addWidget(read_holding_registers_option_third_row_input)
    read_holding_registers_option_parent_layout.addLayout(read_holding_registers_option_third_row_layout)
    read_holding_registers_option_parent_widget.setLayout(read_holding_registers_option_parent_layout)
    additional_options_stacked_widget.addWidget(read_holding_registers_option_parent_widget)

    # Read Input Registers.
    read_input_registers_option_parent_widget = QWidget()
    read_input_registers_option_parent_layout = QVBoxLayout()
    read_input_registers_option_first_row_layout = QHBoxLayout()
    read_input_registers_option_first_row_text = QLabel("First input address(hex):")
    read_input_registers_option_first_row_input = QLineEdit()
    read_input_registers_option_first_row_input.setPlaceholderText("Insert the first input address...")
    read_input_registers_option_first_row_input.setMinimumWidth(300)
    read_input_registers_option_first_row_layout.addWidget(read_input_registers_option_first_row_text)
    read_input_registers_option_first_row_layout.addWidget(read_input_registers_option_first_row_input)
    read_input_registers_option_parent_layout.addLayout(read_input_registers_option_first_row_layout)
    read_input_registers_option_second_row_layout = QHBoxLayout()
    read_input_registers_option_second_row_text = QLabel("Register count(dec):")
    read_input_registers_option_second_row_input = QLineEdit()
    read_input_registers_option_second_row_input.setPlaceholderText("Insert the number of registers...")
    read_input_registers_option_second_row_layout.addWidget(read_input_registers_option_second_row_text)
    read_input_registers_option_second_row_layout.addWidget(read_input_registers_option_second_row_input)
    read_input_registers_option_parent_layout.addLayout(read_input_registers_option_second_row_layout)
    read_input_registers_option_third_row_layout = QHBoxLayout()
    read_input_registers_option_third_row_text = QLabel("Unit Address(dec):")
    read_input_registers_option_third_row_input = QLineEdit()
    read_input_registers_option_third_row_input.setPlaceholderText("Insert the unit address...")
    read_input_registers_option_third_row_layout.addWidget(read_input_registers_option_third_row_text)
    read_input_registers_option_third_row_layout.addWidget(read_input_registers_option_third_row_input)
    read_input_registers_option_parent_layout.addLayout(read_input_registers_option_third_row_layout)
    read_input_registers_option_parent_widget.setLayout(read_input_registers_option_parent_layout)
    additional_options_stacked_widget.addWidget(read_input_registers_option_parent_widget)

    # Write Single Coil.
    write_single_coil_option_parent_widget = QWidget()
    write_single_coil_option_parent_layout = QVBoxLayout()
    write_single_coil_option_first_row_layout = QHBoxLayout()
    write_single_coil_option_first_row_text = QLabel("First coil address(hex):")
    write_single_coil_option_first_row_input = QLineEdit()
    write_single_coil_option_first_row_input.setPlaceholderText("Insert the first coil address...")
    write_single_coil_option_first_row_input.setMinimumWidth(300)
    write_single_coil_option_first_row_layout.addWidget(write_single_coil_option_first_row_text)
    write_single_coil_option_first_row_layout.addWidget(write_single_coil_option_first_row_input)
    write_single_coil_option_parent_layout.addLayout(write_single_coil_option_first_row_layout)
    write_single_coil_option_second_row_layout = QHBoxLayout()
    write_single_coil_option_second_row_text = QLabel("Choose coil state:")
    write_single_coil_option_second_row_input = QComboBox()
    write_single_coil_option_second_row_input.addItem("ON")
    write_single_coil_option_second_row_input.addItem("OFF")
    write_single_coil_option_second_row_layout.addWidget(write_single_coil_option_second_row_text)
    write_single_coil_option_second_row_layout.addWidget(write_single_coil_option_second_row_input)
    write_single_coil_option_parent_layout.addLayout(write_single_coil_option_second_row_layout)
    write_single_coil_option_third_row_layout = QHBoxLayout()
    write_single_coil_option_third_row_text = QLabel("Unit Address(dec):")
    write_single_coil_option_third_row_input = QLineEdit()
    write_single_coil_option_third_row_input.setPlaceholderText("Insert the unit address...")
    write_single_coil_option_third_row_layout.addWidget(write_single_coil_option_third_row_text)
    write_single_coil_option_third_row_layout.addWidget(write_single_coil_option_third_row_input)
    write_single_coil_option_parent_layout.addLayout(write_single_coil_option_third_row_layout)
    write_single_coil_option_parent_widget.setLayout(write_single_coil_option_parent_layout)
    additional_options_stacked_widget.addWidget(write_single_coil_option_parent_widget)

    # Write Single Register.
    write_single_register_option_parent_widget = QWidget()
    write_single_register_option_parent_layout = QVBoxLayout()
    write_single_register_option_first_row_layout = QHBoxLayout()
    write_single_register_option_first_row_text = QLabel("First coil address(hex):")
    write_single_register_option_first_row_input = QLineEdit()
    write_single_register_option_first_row_input.setPlaceholderText("Insert the first coil address...")
    write_single_register_option_first_row_input.setMinimumWidth(300)
    write_single_register_option_first_row_layout.addWidget(write_single_register_option_first_row_text)
    write_single_register_option_first_row_layout.addWidget(write_single_register_option_first_row_input)
    write_single_register_option_parent_layout.addLayout(write_single_register_option_first_row_layout)
    write_single_register_option_second_row_layout = QHBoxLayout()
    write_single_register_option_second_row_text = QLabel("Choose Register value:")
    write_single_register_option_second_row_input = QLineEdit()
    write_single_register_option_second_row_input.setPlaceholderText("Insert the register value...")
    write_single_register_option_second_row_input.setMinimumWidth(300)
    write_single_register_option_second_row_layout.addWidget(write_single_register_option_second_row_text)
    write_single_register_option_second_row_layout.addWidget(write_single_register_option_second_row_input)
    write_single_register_option_parent_layout.addLayout(write_single_register_option_second_row_layout)
    write_single_register_option_third_row_layout = QHBoxLayout()
    write_single_register_option_third_row_text = QLabel("Unit Address(dec):")
    write_single_register_option_third_row_input = QLineEdit()
    write_single_register_option_third_row_input.setPlaceholderText("Insert the unit address...")
    write_single_register_option_third_row_layout.addWidget(write_single_register_option_third_row_text)
    write_single_register_option_third_row_layout.addWidget(write_single_register_option_third_row_input)
    write_single_register_option_parent_layout.addLayout(write_single_register_option_third_row_layout)
    write_single_register_option_parent_widget.setLayout(write_single_register_option_parent_layout)
    additional_options_stacked_widget.addWidget(write_single_register_option_parent_widget)

    left_side_layout.addWidget(additional_options_stacked_widget)
    select_operation_combo_box.activated[int].connect(additional_options_stacked_widget.setCurrentIndex)

    # Submit buttton and it's functionality
    button_submit = QPushButton("Submit")
    button_submit.setStyleSheet("background-color: green")
    button_submit.setFont(font)
    button_submit.sizeHint()
    left_side_layout.addWidget(button_submit)
    button_submit.clicked.connect(
        lambda c: validation.validate_input_data(
            additional_options_stacked_widget.currentIndex(),
            additional_options_stacked_widget.currentWidget(),
            main_widget, request_queue, db_write_queue))

    button_submit.clicked.connect(
        lambda d: right_side_response_init(
            additional_options_stacked_widget.currentIndex(), right_side_layout,
            get_response(response_queue), additional_options_stacked_widget))

    # Right side of the window =========================================================================

    right_side_response_init(-1, right_side_layout, -1, additional_options_stacked_widget)
    # stacked widget for the right side (response)
    response_stacked_widget = QStackedWidget()
    select_operation_combo_box.activated[int].connect(response_stacked_widget.setCurrentIndex)

    middle_vertical_line = QFrame()
    middle_vertical_line.setFixedWidth(20)
    middle_vertical_line.setMinimumHeight(1)
    middle_vertical_line.setFrameShape(QFrame.VLine)
    middle_vertical_line.setFrameShadow(QFrame.Sunken)
    middle_vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

    parent_layout.addLayout(left_side_layout)
    parent_layout.addWidget(middle_vertical_line)
    parent_layout.addLayout(right_side_layout)
    main_widget.setLayout(parent_layout)
    window.setCentralWidget(main_widget)
    window.show()
    app.exec_()


def right_side_response_init(request_code, right_side_layout, response, stacked_widget):
    reset_layout(right_side_layout)

    right_side_layout.setAlignment(QtCore.Qt.AlignTop)

    right_side_label = QLabel("Response:")
    right_side_label.setMinimumWidth(700)
    right_side_label.setMaximumHeight(20)
    right_side_layout.addWidget(right_side_label)

    response_line = QFrame()
    response_line.setFrameShape(QFrame.HLine)
    response_line.setFrameShadow(QFrame.Sunken)
    response_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    right_side_layout.addWidget(response_line)

    response_title_font = QFont("Arial", 12)
    response_title_font.setUnderline(True)

    if  validation.is_valid is False and request_code != -1:
        invalid_data_label = QLabel("Invalid Data.")
        right_side_layout.addWidget(invalid_data_label)
        return

    if request_code == 0 or request_code == 1:
        response_box1 = QHBoxLayout()
        if request_code == 0:
            response_title_label = QLabel("Read coils response: ")
        else:
            response_title_label = QLabel("Read discrete inputs: ")
        response_title_label.setFont(response_title_font)
        response_scroll = QScrollArea()
        response_scroll.setWidgetResizable(True)
        response_scroll.setMaximumHeight(60)
        result_label = QLabel(str(response))
        response_scroll.setWidget(result_label)
        response_box1.addWidget(response_title_label)
        response_box1.addWidget(response_scroll)
        response_box1.setAlignment(QtCore.Qt.AlignTop)
        right_side_layout.addLayout(response_box1)
        response_return_value = process_response(response, stacked_widget)
        response_box2 = QHBoxLayout()
        if len(response_return_value) == 0:
            if request_code == 0:
                response_result_label = QLabel("No Coils Are Set.")
            else:
                response_result_label = QLabel("No Inputs Are Set.")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        elif response_return_value[0] == -1:
            response_result_label = QLabel(response_return_value[1])
            response_result_label.setStyleSheet("color: red")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        else:
            if request_code == 0:
                response_result_label = QLabel("Coils that are set: ")
            else:
                response_result_label = QLabel("Inputs that are set: ")
            response_result_label.setFont(response_title_font)
            response_value_label = QLabel(str(response_return_value))
            response_box2.addWidget(response_result_label)
            response_box2.addWidget(response_value_label)
            right_side_layout.addLayout(response_box2)
        right_side_layout.addStretch()

    elif request_code == 2 or request_code == 3:
        response_box1 = QHBoxLayout()
        if request_code == 2:
            response_title_label = QLabel("Read holding registers response: ")
        else:
            response_title_label = QLabel("Read input registers response: ")
        response_title_label.setFont(response_title_font)
        response_scroll = QScrollArea()
        response_scroll.setWidgetResizable(True)
        response_scroll.setMaximumHeight(60)
        result_label = QLabel(str(response))
        response_scroll.setWidget(result_label)
        response_box1.addWidget(response_title_label)
        response_box1.addWidget(response_scroll)
        response_box1.setAlignment(QtCore.Qt.AlignTop)
        right_side_layout.addLayout(response_box1)
        response_return_value = process_response(response, stacked_widget)
        response_box2 = QHBoxLayout()
        if len(response_return_value) == 0:
            if request_code == 2:
                response_result_label = QLabel("No Holding Registers Are Set.")
            else:
                response_result_label = QLabel("No Input Registers Are Set.")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        elif response_return_value[0] == -1:
            response_result_label = QLabel(response_return_value[1])
            response_result_label.setStyleSheet("color: red")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        else:
            response_result_label = QLabel("Registers(location, value): ")
            response_scroll = QScrollArea()
            response_scroll.setWidgetResizable(True)
            response_scroll.setMaximumHeight(60)
            response_result_label.setFont(response_title_font)
            response_value_label = QLabel(str(response_return_value))
            response_scroll.setWidget(response_value_label)
            response_box2.addWidget(response_result_label)
            response_box2.addWidget(response_scroll)
            right_side_layout.addLayout(response_box2)
        right_side_layout.addStretch()

    elif request_code == 4 or request_code == 5:
        response_box1 = QHBoxLayout()
        if request_code == 4:
            response_title_label = QLabel("Write single coil response: ")
        else:
            response_title_label = QLabel("Write register response: ")
        response_title_label.setFont(response_title_font)
        response_scroll = QScrollArea()
        response_scroll.setWidgetResizable(True)
        response_scroll.setMaximumHeight(60)
        result_label = QLabel(str(response))
        response_scroll.setWidget(result_label)
        response_box1.addWidget(response_title_label)
        response_box1.addWidget(response_scroll)
        response_box1.setAlignment(QtCore.Qt.AlignTop)
        right_side_layout.addLayout(response_box1)
        response_return_value = process_response(response, stacked_widget)
        response_box2 = QHBoxLayout()
        if response_return_value[0] == -1:
            response_result_label = QLabel(response_return_value[1])
            response_result_label.setStyleSheet("color: red")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        else:
            if request_code == 4:
                response_result_label = QLabel("Write single coil was successful")
            else:
                response_result_label = QLabel("Write register was successful")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        right_side_layout.addStretch()


def reset_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            reset_layout(child.layout())


def init_error_window(window, message):
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
