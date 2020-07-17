import sys

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, \
    QHBoxLayout, QSizePolicy, QFrame, QMenu, QMainWindow, QAction

from modbus_gui_app.gui.gui_right_side import right_side_response_init, init_error_window
from modbus_gui_app.gui.gui_left_side import left_side_request_options_init


def start_app(state_manager):
    gui = Gui(state_manager)
    gui.init_gui()


class Gui:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.state_dict = state_manager.get_dict()
        self.right_side_layout = QVBoxLayout()
        self.left_side_layout = QVBoxLayout()
        self.parent_layout = QHBoxLayout()

    def init_gui(self):
        app = QApplication(sys.argv)
        app.setApplicationName("MODBUS")
        window = QMainWindow()
        window.setGeometry(300, 300, 1200, 450)
        main_widget = QWidget()
        font = QFont("Arial", 12)
        main_widget.setFont(font)

        menu_bar = window.menuBar()
        menu = QMenu("History")
        history_action = QAction("Open History")
        history_action.setShortcut("Ctrl+H")
        history_action.setStatusTip("See the history of requests and responses")
        # history_action.triggered.connect(lambda l: self.init_history_window(db_read_queue))
        menu.addAction(history_action)
        menu_bar.addMenu(menu)

        additional_options_stacked_widget, select_operation_combo_box = \
            left_side_request_options_init(self.left_side_layout)

        # Submit buttton and it's functionality
        button_submit = QPushButton("Submit")
        button_submit.setStyleSheet("background-color: green")
        button_submit.setFont(font)
        button_submit.sizeHint()
        self.left_side_layout.addWidget(button_submit)

        button_submit.clicked.connect(lambda c:
                                      self.send_request_data_and_get_response(
                                          additional_options_stacked_widget.currentIndex(),
                                          additional_options_stacked_widget.currentWidget()))

        right_side_response_init(self.right_side_layout, self.state_dict, True, self.parent_layout)
        response_stacked_widget = QStackedWidget()
        select_operation_combo_box.activated[int].connect(response_stacked_widget.setCurrentIndex)

        middle_vertical_line = QFrame()
        middle_vertical_line.setFixedWidth(20)
        middle_vertical_line.setMinimumHeight(1)
        middle_vertical_line.setFrameShape(QFrame.VLine)
        middle_vertical_line.setFrameShadow(QFrame.Sunken)
        middle_vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.parent_layout.addLayout(self.left_side_layout)
        self.parent_layout.addWidget(middle_vertical_line)
        self.parent_layout.addLayout(self.right_side_layout)
        main_widget.setLayout(self.parent_layout)
        window.setCentralWidget(main_widget)
        window.show()
        app.exec_()

    def send_request_data_and_get_response(self, index, stacked_widget):
        self.state_manager.send_request(index, stacked_widget)

        current_request_is_valid = self.state_dict.get("current_request_from_gui_is_valid")

        if current_request_is_valid is True:
            self.state_manager.get_response()

        elif current_request_is_valid is False:
            init_error_window(self.state_dict.get("current_request_from_gui_error_msg"))

        right_side_response_init(self.right_side_layout, self.state_dict, False, self.parent_layout)
