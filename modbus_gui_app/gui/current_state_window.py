from PySide2 import QtCore
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QPushButton

#TODO REGISTERS ROW, + BUTTON ETC...
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

        lower_layout = QVBoxLayout()
        lower_layout.setAlignment(QtCore.Qt.AlignTop)

        underline_font = font
        underline_font.setUnderline(True)

        current_state_header_box = QHBoxLayout()
        current_state_label = QLabel("Current States:")
        current_state_label.setFont(underline_font)
        lower_layout.addWidget(current_state_label)

        current_state_line = QFrame()
        current_state_line.setFrameShape(QFrame.HLine)
        current_state_line.setFrameShadow(QFrame.Sunken)
        current_state_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        lower_layout.addWidget(current_state_line)



        coils_box = QGroupBox()
        select_coil_or_reg_layout = QHBoxLayout()
        select_coil_or_reg_label = QLabel("Coils")
        select_coil_or_reg_label.setFont(underline_font)
        select_coil_or_reg_layout.addWidget(select_coil_or_reg_label)
        coils_box.setLayout(select_coil_or_reg_layout)
        current_state_header_box.addWidget(coils_box)

        select_quantity_box = QGroupBox()
        select_quantity_layout = QHBoxLayout()
        select_quantity_label = QLabel("Start Address(hex)")
        select_quantity_input = QLineEdit()
        select_quantity_input.setPlaceholderText("...")
        select_quantity_input.setMinimumWidth(300)
        select_quantity_layout.addWidget(select_quantity_label)
        select_quantity_layout.addWidget(select_quantity_input)
        select_quantity_layout.addWidget(select_quantity_input)
        select_quantity_box.setLayout(select_quantity_layout)
        current_state_header_box.addWidget(select_quantity_box)


        lower_layout.addLayout(current_state_header_box)

        select_quantity_label1 = QLabel("==================DATA GOES BRRRRR.==================")
        select_quantity_label2 = QLabel("==================DATA GOES BRRRRR.==================")
        select_quantity_label3 = QLabel("==================DATA GOES BRRRRR.==================")
        select_quantity_label4 = QLabel("==================DATA GOES BRRRRR.==================")
        select_quantity_label5 = QLabel("==================DATA GOES BRRRRR.==================")
        lower_layout.addWidget(select_quantity_label1)
        lower_layout.addWidget(select_quantity_label2)
        lower_layout.addWidget(select_quantity_label3)
        lower_layout.addWidget(select_quantity_label4)
        lower_layout.addWidget(select_quantity_label5)

        lower_box.setLayout(lower_layout)
        return lower_box


def update_current_state(coil_or_reg, number_of):
    print("update_current_state")
    print(coil_or_reg, number_of)
