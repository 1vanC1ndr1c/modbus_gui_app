from PySide2 import QtCore
from PySide2.QtGui import QFont, QPalette, Qt
from PySide2.QtWidgets import QLabel, QGroupBox, QVBoxLayout, QScrollArea

from datetime import datetime


class ConnectionInfo:
    def __init__(self, gui, state_manager):
        self.state_manager = state_manager
        self.gui = gui
        self.right_box = QGroupBox()
        self.connection_scroll = QScrollArea()
        self.connection_scroll.setWidgetResizable(True)
        self.connection_scroll.setMinimumWidth(450)
        self.right_box_layout = QVBoxLayout()
        self.connection_font = QFont("Arial", 10)

    def right_side_init(self, right_side_parent_layout):
        self.connection_font.setBold(True)
        self.connection_font.setUnderline(True)

        self.right_box.setStyleSheet("background-color: black")
        self.right_box.setAutoFillBackground(True)
        self.right_box.setFont(self.connection_font)

        connection_header_label = QLabel("Connection info.")
        connection_header_label.setAlignment(QtCore.Qt.AlignTop)
        connection_header_label.setStyleSheet("color: rgb(0, 204,0)")
        connection_header_label.setFont(self.connection_font)

        self.right_box_layout.addWidget(connection_header_label)
        self.right_box.setLayout(self.right_box_layout)
        self.connection_scroll.setWidget(self.right_box)
        right_side_parent_layout.addWidget(self.connection_scroll)

    def connection_established(self, index):
        time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ": "
        if index == 0:
            self.connection_font.setUnderline(False)
            connection_established_time = time + "Connection Established."
            connection_established_label = QLabel(connection_established_time)
            connection_established_label.setAlignment(QtCore.Qt.AlignTop)
            connection_established_label.setStyleSheet("color: rgb(0, 204,0)")
            connection_established_label.setFont(self.connection_font)
            self.right_box_layout.addWidget(connection_established_label)
            self.right_box_layout.addStretch()

        elif index == 1:
            tid = self.state_manager.current_coil_input_reg_states["current_tid"]
            if tid == 9901:
                bytes_req = self.state_manager.current_coil_input_reg_states["current_request"]
                request = time + "Automatic Read Coils Request: " + str(bytes_req)
                auto_read_coils_label = QLabel(request)
                auto_read_coils_label.setAlignment(QtCore.Qt.AlignTop)
                auto_read_coils_label.setStyleSheet("color: rgb(0, 204,0)")
                auto_read_coils_label.setFont(self.connection_font)
                self.right_box_layout.insertWidget(self.right_box_layout.count() - 1, auto_read_coils_label)

            # automatic_request_label = time +
