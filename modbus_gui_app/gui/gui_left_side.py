from PySide2 import QtCore
from PySide2.QtWidgets import QHBoxLayout, QLabel, QComboBox, QStackedWidget, QWidget, QVBoxLayout, QLineEdit, QGroupBox


def left_side_request_options_init(left_side_layout):
    select_operation_box = QGroupBox()
    select_operation_layout = QHBoxLayout()
    select_operation_layout.setAlignment(QtCore.Qt.AlignTop)
    select_operation_label = QLabel("Select an operation:")
    select_operation_layout.addWidget(select_operation_label)
    select_operation_combo_box = QComboBox()
    select_operation_combo_box.addItem("Read Coils")
    select_operation_combo_box.addItem("Read Discrete Inputs")
    select_operation_combo_box.addItem("Read Holding Registers")
    select_operation_combo_box.addItem("Read Input Registers")
    select_operation_combo_box.addItem("Write Single Coil")
    select_operation_combo_box.addItem("Write Single Register")
    select_operation_layout.addWidget(select_operation_combo_box)
    select_operation_box.setLayout(select_operation_layout)
    left_side_layout.addWidget(select_operation_box)

    additional_options_stacked_widget = QStackedWidget()

    read_coils_option_parent_widget = create_read_coils_section()
    additional_options_stacked_widget.addWidget(read_coils_option_parent_widget)

    read_discrete_inputs_option_parent_widget = create_read_discrete_inputs_section()
    additional_options_stacked_widget.addWidget(read_discrete_inputs_option_parent_widget)

    read_holding_registers_option_parent_widget = create_read_holding_registers_section()
    additional_options_stacked_widget.addWidget(read_holding_registers_option_parent_widget)

    read_input_registers_option_parent_widget = create_read_input_registers_section()
    additional_options_stacked_widget.addWidget(read_input_registers_option_parent_widget)

    write_single_coil_option_parent_widget = create_write_single_coil_option_section()
    additional_options_stacked_widget.addWidget(write_single_coil_option_parent_widget)

    write_single_register_option_parent_widget = create_write_single_register_section()
    additional_options_stacked_widget.addWidget(write_single_register_option_parent_widget)

    left_side_layout.addWidget(additional_options_stacked_widget, 0, QtCore.Qt.AlignTop)
    select_operation_combo_box.activated[int].connect(additional_options_stacked_widget.setCurrentIndex)

    left_size_constraint_widget = QWidget()
    left_size_constraint_widget.setMaximumWidth(600)
    left_size_constraint_widget.setMaximumHeight(300)
    left_size_constraint_widget.setLayout(left_side_layout)

    return left_size_constraint_widget, additional_options_stacked_widget, select_operation_combo_box


def create_read_coils_section():
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

    return read_coils_option_parent_widget


def create_read_discrete_inputs_section():
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

    return read_discrete_inputs_option_parent_widget


def create_read_holding_registers_section():
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

    return read_holding_registers_option_parent_widget


def create_read_input_registers_section():
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

    return read_input_registers_option_parent_widget


def create_write_single_coil_option_section():
    write_single_coil_option_parent_widget = QWidget()
    write_single_coil_option_parent_layout = QVBoxLayout()

    write_single_coil_option_first_row_layout = QHBoxLayout()
    write_single_coil_option_first_row_text = QLabel("Coil address(hex):")
    write_single_coil_option_first_row_input = QLineEdit()
    write_single_coil_option_first_row_input.setPlaceholderText("Insert the coil address...")
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

    return write_single_coil_option_parent_widget


def create_write_single_register_section():
    write_single_register_option_parent_widget = QWidget()
    write_single_register_option_parent_layout = QVBoxLayout()

    write_single_register_option_first_row_layout = QHBoxLayout()
    write_single_register_option_first_row_text = QLabel("Register address(hex):")
    write_single_register_option_first_row_input = QLineEdit()
    write_single_register_option_first_row_input.setPlaceholderText("Insert the register address...")
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

    return write_single_register_option_parent_widget
