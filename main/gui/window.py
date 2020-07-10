import sys

from PySide2 import QtCore
from PySide2.QtCore import QRect
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QPushButton, QStackedWidget, \
    QHBoxLayout, QLineEdit, QDialog, QSpacerItem, QSizePolicy, QFrame

import validation
from response_processing import process_response, get_response


def init_gui(request_queue, response_queue):
    app = QApplication(sys.argv)
    app.setApplicationName("MODBUS")
    window = QWidget()
    window.setGeometry(300, 300, 1200, 450)
    font = QFont("Arial", 12)
    window.setFont(font)
    parent_layout = QHBoxLayout()
    right_side_layout = QVBoxLayout()
    left_side_layout = QVBoxLayout()

    # Left side of the window =========================================================================================
    select_operation_layout = QHBoxLayout()
    select_operation_label = QLabel("Select an operation:")
    select_operation_layout.addWidget(select_operation_label)
    select_operation_combo_box = QComboBox()
    select_operation_combo_box.addItem("Read Coils")
    select_operation_combo_box.addItem("Read Discrete Inputs")
    select_operation_combo_box.addItem("not impl2")
    select_operation_combo_box.addItem("not impl3")
    select_operation_combo_box.addItem("not impl4")
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

    # TODO add options for other instructions

    # Read Discrete Inputs.
    read_discrete_inputs_option_parent_widget = QWidget()
    read_discrete_inputs_option_parent_layout = QVBoxLayout()
    # read_discrete_inputs_option_first_row_layout = QHBoxLayout()
    # read_discrete_inputs_option_first_row_text = QLabel("First input address(hex):")
    # read_discrete_inputs_option_first_row_input = QLineEdit()
    # read_discrete_inputs_option_first_row_input.setPlaceholderText("Insert the first input address...")
    # read_discrete_inputs_option_first_row_input.setMinimumWidth(300)
    # read_discrete_inputs_option_first_row_layout.addWidget(read_discrete_inputs_option_first_row_text)
    # read_discrete_inputs_option_first_row_layout.addWidget(read_discrete_inputs_option_first_row_input)
    # read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_first_row_layout)
    # read_discrete_inputs_option_second_row_layout = QHBoxLayout()
    # read_discrete_inputs_option_second_row_text = QLabel("Register count(dec):")
    # read_discrete_inputs_option_second_row_input = QLineEdit()
    # read_discrete_inputs_option_second_row_input.setPlaceholderText("Insert the number of registers...")
    # read_discrete_inputs_option_second_row_layout.addWidget(read_discrete_inputs_option_second_row_text)
    # read_discrete_inputs_option_second_row_layout.addWidget(read_discrete_inputs_option_second_row_input)
    # read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_second_row_layout)
    # read_discrete_inputs_option_third__row_layout = QHBoxLayout()
    # read_discrete_inputs_option_third__row_text = QLabel("Unit Address(dec):")
    # read_discrete_inputs_option_third__row_input = QLineEdit()
    # read_discrete_inputs_option_third__row_input.setPlaceholderText("Insert the unit address...")
    # read_discrete_inputs_option_third__row_layout.addWidget(read_discrete_inputs_option_third__row_text)
    # read_discrete_inputs_option_third__row_layout.addWidget(read_discrete_inputs_option_third__row_input)
    # read_discrete_inputs_option_parent_layout.addLayout(read_discrete_inputs_option_third__row_layout)
    # read_discrete_inputs_option_parent_widget.setLayout(read_discrete_inputs_option_parent_layout)
    additional_options_stacked_widget.addWidget(read_discrete_inputs_option_parent_widget)

    # Other options

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
            window, request_queue))
    button_submit.clicked.connect(
        lambda d: right_side_response_init(
            additional_options_stacked_widget.currentIndex(), right_side_layout,
            get_response(response_queue), additional_options_stacked_widget)) # TODO REQ queue here is the error

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
    window.setLayout(parent_layout)
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

    if validation.is_valid is False and request_code != -1:
        invalid_data_label = QLabel("Invalid Data.")
        right_side_layout.addWidget(invalid_data_label)
        return

    if request_code == 0:

        response_box1 = QHBoxLayout()
        response_title_label = QLabel("Read coils response: ")
        response_title_label.setFont(response_title_font)
        result_label = QLabel(str(response))
        response_box1.addWidget(response_title_label)
        response_box1.addWidget(result_label)

        right_side_layout.addLayout(response_box1)

        indices = process_response(response, stacked_widget)

        if len(indices) == 0:
            response_result_label = QLabel("No Coils Are Set.")
            response_result_label.setFont(response_title_font)
            right_side_layout.addWidget(response_result_label)
        else:
            response_box2 = QHBoxLayout()
            response_result_label = QLabel("Coils that are set: ")
            response_result_label.setFont(response_title_font)
            response_value_label = QLabel(str(indices))
            response_box2.addWidget(response_result_label)
            response_box2.addWidget(response_value_label)
            right_side_layout.addLayout(response_box2)


def reset_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            reset_layout(child.layout())


def init_error_window(window, message):
    error_dlg_window = QDialog(window)
    error_dlg_window.setWindowTitle("ERROR")
    error_font = QFont("Arial", 12)
    error_label = QLabel(message)
    error_label.setStyleSheet("color: red")
    error_label.setFont(error_font)
    error_layout = QVBoxLayout()
    error_layout.addWidget(error_label)
    error_dlg_window.setLayout(error_layout)
    error_dlg_window.exec_()
