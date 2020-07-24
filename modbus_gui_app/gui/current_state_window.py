from PySide2 import QtCore
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QPushButton, QScrollArea

from modbus_gui_app.logic.state_manager import StateManager


# TODO DONT DO STUFF UNTIL REVIEW 2 IS PROCESSED
class CurrentStateWindow:

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.isFirst = True
        self.more_data = []
        self.last_ten_dicts = []
        self.rows = None
        self.table_view = None

    def init_current_state_window(self, font):
        lower_box = QGroupBox()
        # parent_layout = QVBoxLayout()
        # parent_layout.setAlignment(QtCore.Qt.AlignTop)
        # underline_font = QFont("Arial", 12)
        # underline_font.setUnderline(True)
        # lower_layout = QHBoxLayout()
        #
        # # coil box
        # coils_parent_box = QGroupBox()
        # coils_parent_layout = QVBoxLayout()
        # coils_label = QLabel("Coil Status")
        # coils_label.setFont(underline_font)
        # coils_label.setAlignment(QtCore.Qt.AlignCenter)
        # coils_label.setFont(underline_font)
        # coils_parent_layout.addWidget(coils_label)
        # coils_parent_box.setLayout(coils_parent_layout)
        # coils_second_row_layout = QHBoxLayout()
        # coil_select_box = QGroupBox()
        # coil_select_box.setMaximumWidth(350)
        # coil_select_layout = QHBoxLayout()
        # coil_select_layout.setAlignment(QtCore.Qt.AlignTop)
        # coil_select_label = QLabel("Start Address(hex):")
        # coil_select_layout.addWidget(coil_select_label)
        # coil_input = QLineEdit()
        # coil_input.setAlignment(QtCore.Qt.AlignLeft)
        # coil_input.setPlaceholderText("Insert...")
        # coil_select_layout.addWidget(coil_input)
        # coil_select_box.setLayout(coil_select_layout)
        # coils_second_row_layout.addWidget(coil_select_box)
        # coils_parent_layout.addLayout(coils_second_row_layout)
        # coil_submit_button = QPushButton("Submit")
        # coil_submit_button.setMaximumWidth(80)
        # coil_submit_button.setStyleSheet("background-color: green")
        # coil_submit_button.setFont(font)
        # coils_second_row_layout.addWidget(coil_submit_button)
        # coil_scroll = QScrollArea()
        # coil_scroll.setMaximumHeight(500)
        # coil_scroll.setWidgetResizable(True)
        # coil_result_label = QLabel("TODO PUT COIL STATUS HERE\n"
        #                            "sadasdsds\n"
        #                            "czfdfsdffdsv\n""sadasdsds\n""sadasdsds\n"
        #                            "sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n"
        #                            "sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n"
        #                            "sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n"
        #                            "sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n"
        #                            "sadasdsds\n""sadasdsds\n""sadasdsds\n""sadasdsds\n")
        # coil_scroll.setWidget(coil_result_label)
        # coils_parent_layout.addWidget(coil_scroll)
        # coil_more_button_layout = QHBoxLayout()
        # coil_more_button_layout.addStretch()
        # coil_more_button = QPushButton("More")
        # coil_more_button.setMaximumWidth(80)
        # coil_more_button.setStyleSheet("background-color: green")
        # coil_more_button.setFont(font)
        # coil_more_button_layout.addWidget(coil_more_button)
        # coil_more_button_layout.addStretch()
        # coils_parent_layout.addLayout(coil_more_button_layout)
        # lower_layout.addWidget(coils_parent_box)
        #
        # # TODO read the data from the input field
        # coil_submit_button.clicked.connect(lambda l: self.state_manager.update_current_window(
        #     "READ_COILS", coil_input.text(), 50))
        # coil_more_button.clicked.connect(lambda l: self.state_manager.current_window_more_data("READ_COILS"))
        #
        # lower_layout.addStretch()
        # lower_layout.addStretch()
        # lower_layout.addStretch()
        # parent_layout.addLayout(lower_layout)
        # lower_box.setLayout(parent_layout)
        return lower_box
