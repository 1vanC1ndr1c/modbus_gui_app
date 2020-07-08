import sys

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QPushButton, QStackedWidget, \
    QHBoxLayout, QLineEdit, QDialog

from logic.request_processing import process_request


def init_gui():
    app = QApplication(sys.argv)
    app.setApplicationName("MODBUS")
    window = QWidget()
    window.setGeometry(300, 300, 800, 450)
    font = QFont("Arial", 12)
    window.setFont(font)
    parent_layout = QHBoxLayout()
    parent_layout.minimumSize()
    left_side_layout = QVBoxLayout()
    right_side_layout = QVBoxLayout()

    select_operation_layout = QHBoxLayout()
    select_operation_label = QLabel("Select an operation:")
    select_operation_layout.addWidget(select_operation_label)
    select_operation_combo_box = QComboBox()
    select_operation_combo_box.addItem("Read Coils")
    select_operation_combo_box.addItem("not impl1")
    select_operation_combo_box.addItem("not impl2")
    select_operation_combo_box.addItem("not impl3")
    select_operation_combo_box.addItem("not impl4")
    select_operation_layout.addWidget(select_operation_combo_box)
    left_side_layout.addLayout(select_operation_layout)

    # Create additional options based on the selected options in the drop down menu.
    additional_options_stacked_widget = QStackedWidget()

    read_coils_option_parent_widget = QWidget()
    read_coils_option_parent_layout = QVBoxLayout()
    read_coils_option_first_row_layout = QHBoxLayout()
    read_coils_option_first_row_text = QLabel("Starting Address:")
    read_coils_option_first_row_input = QLineEdit()
    read_coils_option_first_row_input.setPlaceholderText("Insert the starting address...")
    read_coils_option_first_row_layout.addWidget(read_coils_option_first_row_text)
    read_coils_option_first_row_layout.addWidget(read_coils_option_first_row_input)
    read_coils_option_parent_layout.addLayout(read_coils_option_first_row_layout)
    read_coils_option_second_row_layout = QHBoxLayout()
    read_coils_option_second_row_text = QLabel("Number of coils:")
    read_coils_option_second_row_input = QLineEdit()
    read_coils_option_second_row_input.setPlaceholderText("Insert the number of coils...")
    read_coils_option_second_row_layout.addWidget(read_coils_option_second_row_text)
    read_coils_option_second_row_layout.addWidget(read_coils_option_second_row_input)
    read_coils_option_parent_layout.addLayout(read_coils_option_second_row_layout)
    read_coils_option_parent_widget.setLayout(read_coils_option_parent_layout)

    # TODO add options for other instructions

    additional_options_stacked_widget.addWidget(read_coils_option_parent_widget)

    widget_other_option = QWidget()
    additional_options_stacked_widget.addWidget(widget_other_option)

    left_side_layout.addWidget(additional_options_stacked_widget)
    select_operation_combo_box.activated[int].connect(additional_options_stacked_widget.setCurrentIndex)

    button_submit = QPushButton("Submit")
    button_submit.setStyleSheet("background-color: green")
    button_submit.setFont(font)
    button_submit.sizeHint()
    left_side_layout.addWidget(button_submit)

    # TODO pass arguments into this function
    button_submit.clicked.connect(
        lambda c: validate_input_data_and_produce_a_response(
            additional_options_stacked_widget.currentIndex(),
            additional_options_stacked_widget.currentWidget(),
            window))

    parent_layout.addLayout(left_side_layout)
    parent_layout.addLayout(right_side_layout)
    window.setLayout(parent_layout)
    window.show()
    app.exec_()


def validate_input_data_and_produce_a_response(index, stackedWidget, window):
    if index == 0:  # read coils, 2 inputs (starting address and no. of coils)
        inputs = stackedWidget.findChildren(QLineEdit)  # get children that are used for data input
        for index, inp in enumerate(inputs):
            try:
                if index == 0:  # check the validity of the first input
                    start_address_hex = int(str(inp.text()), 16)
                    if start_address_hex < 0x0000 or start_address_hex > 0xFFFF:
                        init_error_window(window)
                    else:
                        process_request()


            except:
                init_error_window(window)

    # print("YOLO")


def init_error_window(window):
    error_dlg_window = QDialog(window)
    error_dlg_window.setWindowTitle("ERROR")
    error_font = QFont("Arial", 12)
    error_label = QLabel("Error, Wrong values were given.")
    error_label.setStyleSheet("color: red")
    error_label.setFont(error_font)
    error_layout = QVBoxLayout()
    error_layout.addWidget(error_label)
    error_dlg_window.setLayout(error_layout)
    error_dlg_window.exec_()