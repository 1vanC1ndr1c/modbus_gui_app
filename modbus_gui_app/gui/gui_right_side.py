from PySide2.QtWidgets import QLabel


def right_side_init(right_side_layout):
    right_label = QLabel("TODO show connection info here.")
    right_label2 = QLabel("sent and received messages and their reasons")

    right_side_layout.addWidget(right_label)
    right_side_layout.addWidget(right_label2)
