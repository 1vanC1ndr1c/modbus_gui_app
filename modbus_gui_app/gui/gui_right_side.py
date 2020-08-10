from datetime import datetime

from PySide2 import QtCore
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel, QGroupBox, QVBoxLayout, QScrollArea

from modbus_gui_app.gui.gui_middle import reset_layout


class ConnectionInfo:
    def __init__(self, gui, state_manager):
        self._state_manager = state_manager
        self.gui = gui
        self._right_box = QGroupBox()
        self._connection_scroll = QScrollArea()
        self._connection_scroll.setWidgetResizable(True)
        self._connection_scroll.setMinimumWidth(450)
        self._right_box_layout = QVBoxLayout()
        self._connection_font = QFont("Arial", 10)
        self._auto_request_label = _QCustomConnectionLabel("")
        self._auto_response_label = _QCustomConnectionLabel("")

    def right_side_init(self, right_side_parent_layout):
        self._connection_font.setBold(True)
        self._connection_font.setUnderline(True)

        self._right_box.setStyleSheet("background-color: black")
        self._right_box.setAutoFillBackground(True)
        self._right_box.setFont(self._connection_font)

        connection_header_label = QLabel("Connection info.")
        connection_header_label.setAlignment(QtCore.Qt.AlignTop)
        connection_header_label.setStyleSheet("color: rgb(0, 204,0)")
        connection_header_label.setFont(self._connection_font)
        self._right_box_layout.addWidget(connection_header_label)

        self._right_box.setLayout(self._right_box_layout)
        self._connection_scroll.setWidget(self._right_box)
        right_side_parent_layout.addWidget(self._connection_scroll)

    def generate_connection_info(self, msg):
        time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": "

        if msg == "Connection Established":
            self._connection_established_msg_show(time)
        elif msg == "Automatic Request Sent.":
            self._auto_request_msg_show(time)
        elif msg == "Automatic Request Received.":
            self._auto_response_msg_show(time)
        elif msg == "User Request Sent.":
            self._user_request_msg_show(time)
        elif msg == "User Response Received.":
            self._user_response_msg_show(time)
        elif msg == "No Connection.":
            reset_layout(self._right_box_layout)
            self._connection_font.setUnderline(True)
            connection_header_label = QLabel("Connection info.")
            connection_header_label.setAlignment(QtCore.Qt.AlignTop)
            connection_header_label.setStyleSheet("color: rgb(0, 204,0)")
            connection_header_label.setFont(self._connection_font)
            self._right_box_layout.addWidget(connection_header_label)
            self._right_box_layout.addWidget(_QCustomConnectionLabel("ERROR: Connection not established."))
            self._right_box_layout.addStretch()

    def _connection_established_msg_show(self, time):
        self._connection_font.setUnderline(False)
        connection_established_time = time + "Connection Established."
        connection_established_label = _QCustomConnectionLabel(connection_established_time)
        self._right_box_layout.addWidget(connection_established_label)
        self._right_box_layout.insertWidget(2, self._auto_request_label)
        self._right_box_layout.insertWidget(3, self._auto_response_label)
        self._right_box_layout.addStretch()

    def _auto_request_msg_show(self, time):
        auto_request_type = "Unknown Request."
        f_code = self._state_manager.live_update_states["currently_selected_function"]
        auto_bytes_req = b'0'
        if f_code == "01":
            auto_bytes_req = self._state_manager.live_update_states["current_read_coils"]
            auto_bytes_req = auto_bytes_req["current_request_serialized"]
            auto_request_type = "Automatic Read Coils Request:"
        elif f_code == "02":
            auto_bytes_req = self._state_manager.live_update_states["current_read_discrete_inputs"]
            auto_bytes_req = auto_bytes_req["current_request_serialized"]
            auto_request_type = "Automatic Read Discrete Inputs Request:"
        elif f_code == "03":
            auto_bytes_req = self._state_manager.live_update_states["current_read_holding_registers"]
            auto_bytes_req = auto_bytes_req["current_request_serialized"]
            auto_request_type = "Automatic Read Holding Registers Request:"
        elif f_code == "04":
            auto_bytes_req = self._state_manager.live_update_states["current_read_input_registers"]
            auto_bytes_req = auto_bytes_req["current_request_serialized"]
            auto_request_type = "Automatic Read Input Registers Request:"
        auto_request = _get_str_separator() + "\n" + time + auto_request_type + " " + str(auto_bytes_req)
        self._auto_request_label.setText(auto_request)

    def _auto_response_msg_show(self, time):
        auto_response_type = "Unknown Response."
        auto_bytes_resp = b'0'
        f_code = self._state_manager.live_update_states["currently_selected_function"]
        if f_code == "01":
            auto_response_type = "Automatic Read Coils Response:"
            auto_bytes_resp = self._state_manager.live_update_states["current_read_coils"]
            auto_bytes_resp = auto_bytes_resp["current_response_serialized"]
        elif f_code == "02":
            auto_response_type = "Automatic Read Discrete Inputs Response:"
            auto_bytes_resp = self._state_manager.live_update_states["current_read_discrete_inputs"]
            auto_bytes_resp = auto_bytes_resp["current_response_serialized"]
        elif f_code == "03":
            auto_response_type = "Automatic Read Holding Registers Response:"
            auto_bytes_resp = self._state_manager.live_update_states["current_read_holding_registers"]
            auto_bytes_resp = auto_bytes_resp["current_response_serialized"]
        elif f_code == "04":
            auto_response_type = "Automatic Read Input Registers Response:"
            auto_bytes_resp = self._state_manager.live_update_states["current_read_input_registers"]
            auto_bytes_resp = auto_bytes_resp["current_response_serialized"]

        auto_response = time + auto_response_type + " " + str(auto_bytes_resp) + "\n" + _get_str_separator()
        self._auto_response_label.setText(auto_response)

    def _user_request_msg_show(self, time):
        f_code = self._state_manager.user_action_state["current_function_code"]
        user_request_type = "Unknown Request."
        user_bytes_req = self._state_manager.user_action_state
        user_bytes_req = user_bytes_req["current_request_serialized"]
        if f_code == "01":
            user_request_type = "User Read Coils Request:"
        elif f_code == "02":
            user_request_type = "User Read Discrete Inputs Request:"
        elif f_code == "03":
            user_request_type = "User Read Holding Registers Request:"
        elif f_code == "04":
            user_request_type = "User Read Input Registers Request:"
        elif f_code == "05":
            user_request_type = "User Write Single Coil Request:"
        elif f_code == "06":
            user_request_type = "User Write Single Register Request:"

        user_request = time + user_request_type + " " + str(user_bytes_req)
        user_request_label = _QCustomConnectionLabel(user_request)
        self._right_box_layout.insertWidget(self._right_box_layout.count() - 1, user_request_label)

    def _user_response_msg_show(self, time):
        f_code = self._state_manager.user_action_state["current_function_code"]
        user_response_type = "Unknown Response."
        user_bytes_resp = self._state_manager.user_action_state
        user_bytes_resp = user_bytes_resp["current_response_serialized"]
        if f_code == "01":
            user_response_type = "User Read Coils Response:"
        elif f_code == "02":
            user_response_type = "User Read Discrete Inputs Response:"
        elif f_code == "03":
            user_response_type = "User Read Holding Registers Response:"
        elif f_code == "04":
            user_response_type = "User Read Input Registers Response:"
        elif f_code == "05":
            user_response_type = "User Write Single Coil Response:"
        elif f_code == "06":
            user_response_type = "User Write Single Register Response:"

        user_response = time + user_response_type + " " + str(user_bytes_resp)
        user_response_label = _QCustomConnectionLabel(user_response)
        self._right_box_layout.insertWidget(self._right_box_layout.count() - 1, user_response_label)


class _QCustomConnectionLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self._connection_font = QFont("Arial", 10)
        self._connection_font.setBold(True)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setStyleSheet("color: rgb(0, 204,0)")
        self.setFont(self._connection_font)


def _get_str_separator():
    return "--------------------" \
           + "--------------------" \
           + "--------------------" \
           + "--------------------" \
           + "--------------------" \
           + "--------------------" \
           + "--------------------"
