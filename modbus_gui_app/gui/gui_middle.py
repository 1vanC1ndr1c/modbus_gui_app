from PySide2.QtWidgets import QLabel, QHBoxLayout, QScrollArea, QDialog, QVBoxLayout, QGroupBox
from PySide2.QtGui import QFont
from PySide2 import QtCore


def middle_init(mid_layout, dictionary, first_init):
    reset_layout(mid_layout)

    mid_layout.setAlignment(QtCore.Qt.AlignTop)

    middle_header_box = QGroupBox()
    middle_header_box.setAlignment(QtCore.Qt.AlignTop)
    middle_label = QLabel("Response:")
    middle_label.setAlignment(QtCore.Qt.AlignTop)
    middle_label.setMinimumWidth(700)

    middle_header_layout = QVBoxLayout()
    middle_header_layout.setAlignment(QtCore.Qt.AlignTop)
    middle_header_layout.addWidget(middle_label)
    middle_header_box.setLayout(middle_header_layout)
    mid_layout.addWidget(middle_header_box)

    u_font = QFont("Arial", 12)
    u_font.setUnderline(True)

    request_is_valid = dictionary.get("current_request_from_gui_is_valid")
    if request_is_valid is False and first_init is False:
        invalid_data_label = QLabel("Invalid Data.")
        mid_layout.addWidget(invalid_data_label)
        return

    if first_init is False:
        function_code = dictionary.get("current_request_from_gui")[3]
    else:
        function_code = -1

    resp = dictionary.get("current_response_serialized")
    is_valid_resp = dictionary.get("current_response_is_valid")
    err_msg = dictionary.get("current_response_err_msg")

    if function_code == 1:
        read_coils_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)
    elif function_code == 2:
        read_discrete_inputs_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)
    elif function_code == 3:
        read_holding_registers_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)
    elif function_code == 4:
        read_input_registers_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)
    elif function_code == 5:
        write_single_coil_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)
    elif function_code == 6:
        write_single_register_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg)


def read_coils_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Read coils response: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_return_value = dictionary.get("current_response_returned_values")
    response_box2 = QHBoxLayout()

    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    elif response_return_value == "-":
        response_result_label = QLabel("No Coils Are Set.")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Coils that are set: ")
        response_result_label.setFont(u_font)
        response_value_label = QLabel(str(response_return_value))
        response_box2.addWidget(response_result_label)
        response_box2.addWidget(response_value_label)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def read_discrete_inputs_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Read discrete inputs: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_return_value = dictionary.get("current_response_returned_values")
    response_box2 = QHBoxLayout()

    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    elif response_return_value == "-":
        response_result_label = QLabel("No Inputs Are Set.")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Inputs that are set: ")
        response_result_label.setFont(u_font)
        response_value_label = QLabel(str(response_return_value))
        response_box2.addWidget(response_result_label)
        response_box2.addWidget(response_value_label)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def read_holding_registers_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Read holding registers response: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_return_value = dictionary.get("current_response_returned_values")

    response_box2 = QHBoxLayout()
    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    elif response_return_value == "-":
        response_result_label = QLabel("No Holding Registers Are Set.")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Registers(location, value): ")
        response_scroll = QScrollArea()
        response_scroll.setWidgetResizable(True)
        response_scroll.setMaximumHeight(60)
        response_result_label.setFont(u_font)
        response_value_label = QLabel(str(response_return_value))
        response_scroll.setWidget(response_value_label)
        response_box2.addWidget(response_result_label)
        response_box2.addWidget(response_scroll)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def read_input_registers_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Read input registers response: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_return_value = dictionary.get("current_response_returned_values")

    response_box2 = QHBoxLayout()
    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    elif response_return_value == "-":
        response_result_label = QLabel("No Input Registers Are Set.")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Registers(location, value): ")
        response_scroll = QScrollArea()
        response_scroll.setWidgetResizable(True)
        response_scroll.setMaximumHeight(60)
        response_result_label.setFont(u_font)
        response_value_label = QLabel(str(response_return_value))
        response_scroll.setWidget(response_value_label)
        response_box2.addWidget(response_result_label)
        response_box2.addWidget(response_scroll)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def write_single_coil_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Write single coil response: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_box2 = QHBoxLayout()
    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Write single coil was successful")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def write_single_register_generate_response_widget(u_font, resp, mid_layout, dictionary, is_valid_resp, err_msg):
    response_box1 = QHBoxLayout()
    response_title_label = QLabel("Write register response: ")
    response_title_label.setFont(u_font)
    response_scroll = QScrollArea()
    response_scroll.setWidgetResizable(True)
    response_scroll.setMaximumHeight(60)
    result_label = QLabel(str(resp))
    response_scroll.setWidget(result_label)
    response_box1.addWidget(response_title_label)
    response_box1.addWidget(response_scroll)
    response_box1.setAlignment(QtCore.Qt.AlignTop)
    mid_layout.addLayout(response_box1)
    response_box2 = QHBoxLayout()
    if is_valid_resp is False:
        response_result_label = QLabel(err_msg)
        response_result_label.setStyleSheet("color: red")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    else:
        response_result_label = QLabel("Write register was successful")
        response_result_label.setFont(u_font)
        response_box2.addWidget(response_result_label)
        mid_layout.addLayout(response_box2)
    mid_layout.addStretch()


def reset_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            reset_layout(child.layout())


