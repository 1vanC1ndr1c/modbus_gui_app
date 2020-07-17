from PySide2.QtWidgets import QLabel, QFrame, QSizePolicy, QHBoxLayout, QScrollArea, QDialog, QVBoxLayout
from PySide2.QtGui import QFont
from PySide2 import QtCore


def right_side_response_init(right_side_layout, dictionary, first_init, parent_layout):
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

    request_is_valid = dictionary.get("current_request_from_gui_is_valid")
    if request_is_valid is False and first_init is False:
        invalid_data_label = QLabel("Invalid Data.")
        right_side_layout.addWidget(invalid_data_label)
        return

    if first_init is False:
        function_code = dictionary.get("current_request_from_gui")[3]
    else:
        function_code = -1

    response = dictionary.get("current_response_serialized")

    if function_code == 1 or function_code == 2:
        response_box1 = QHBoxLayout()
        if function_code == 1:
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
        response_return_value = dictionary.get("current_response_returned_values")
        response_box2 = QHBoxLayout()
        if response_return_value == "/":
            if function_code == 1:
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
            if function_code == 1:
                response_result_label = QLabel("Coils that are set: ")
            else:
                response_result_label = QLabel("Inputs that are set: ")
            response_result_label.setFont(response_title_font)
            response_value_label = QLabel(str(response_return_value))
            response_box2.addWidget(response_result_label)
            response_box2.addWidget(response_value_label)
            right_side_layout.addLayout(response_box2)
        right_side_layout.addStretch()

    elif function_code == 3 or function_code == 4:
        response_box1 = QHBoxLayout()
        if function_code == 3:
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
        response_return_value = dictionary.get("current_response_returned_values")

        response_box2 = QHBoxLayout()
        if response_return_value == "/":
            if function_code == 3:
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

    elif function_code == 5 or function_code == 6:
        response_box1 = QHBoxLayout()
        if function_code == 5:
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
        response_return_value = dictionary.get("current_response_returned_values")
        response_box2 = QHBoxLayout()
        if response_return_value[0] == -1:
            response_result_label = QLabel(response_return_value[1])
            response_result_label.setStyleSheet("color: red")
            response_result_label.setFont(response_title_font)
            response_box2.addWidget(response_result_label)
            right_side_layout.addLayout(response_box2)
        else:
            if function_code == 5:
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


def init_error_window(message):
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
