from PySide2 import QtCore
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QPushButton, QScrollArea, QStackedWidget

from modbus_gui_app.logic.validation import validate_current_state_data
from modbus_gui_app.gui.error_window import init_error_window


# TODO DONT DO STUFF UNTIL REVIEW 2 IS PROCESSED
class CurrentStateWindow:

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.isFirst = True
        self.more_data = []
        self.last_ten_dicts = []
        self.rows = None
        self.table_view = None

    def init_current_state_window(self, font, left_side_select_operation_box):
        # TODO change the lower window based on the currently selected option
        lower_box = QGroupBox()
        parent_layout = QVBoxLayout()
        parent_layout.setAlignment(QtCore.Qt.AlignTop)
        underline_font = QFont("Arial", 12)
        underline_font.setUnderline(True)

        current_state_stacked_widget = QStackedWidget()
        read_coils_current_state_widget = QLabel("READ COILS")
        current_state_stacked_widget.addWidget(read_coils_current_state_widget)
        other_current_state_widget = QLabel("OTHER")
        current_state_stacked_widget.addWidget(other_current_state_widget)

        parent_layout.addWidget(read_coils_current_state_widget)
        lower_box.setLayout(parent_layout)

        return lower_box
