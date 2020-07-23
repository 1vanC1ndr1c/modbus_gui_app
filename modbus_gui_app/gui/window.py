import sys

from PySide2 import QtCore
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, \
    QHBoxLayout, QSizePolicy, QFrame, QMenu, QMainWindow, QAction, QStyleFactory, QGroupBox, QLayout

from modbus_gui_app.gui.gui_middle import middle_response_init, init_error_window
from modbus_gui_app.gui.gui_left_side import left_side_request_options_init
from modbus_gui_app.gui.gui_right_side import right_side_init
from modbus_gui_app.gui.current_state_window import CurrentStateWindow
from modbus_gui_app.gui.history_window import HistoryWindow


def start_app(state_manager):
    gui = Gui(state_manager)
    gui.init_gui()


class Gui:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.state_dict = state_manager.get_dict()
        self.left_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.parent_layout = QVBoxLayout()
        self.upper_layout = QHBoxLayout()
        self.history_window = HistoryWindow(state_manager)
        self.current_state_window = CurrentStateWindow(state_manager)

    def init_gui(self):
        app = QApplication(sys.argv)
        app_icon = QIcon()
        app_icon.addFile("resources/main_window_16px.png", QtCore.QSize(16, 16))
        app_icon.addFile("resources/main_window_24px.png", QtCore.QSize(24, 24))
        app_icon.addFile("resources/main_window_32px.png", QtCore.QSize(32, 32))
        app_icon.addFile("resources/main_window_48px.png", QtCore.QSize(48, 48))
        app_icon.addFile("resources/main_window_256px.png", QtCore.QSize(256, 256))
        app.setWindowIcon(app_icon)

        app.setStyle("fusion")
        app.setApplicationName("MODBUS")
        window = QMainWindow()
        window.setGeometry(300, 300, 1200, 450)
        main_widget = QWidget()
        font = QFont("Arial", 12)
        main_widget.setFont(font)
        self.parent_layout.setStretchFactor(self.left_layout, 0)
        self.parent_layout.setAlignment(QtCore.Qt.AlignLeft)

        menu_bar = window.menuBar()
        history_menu = QMenu("History")
        history_action = QAction("Open History")
        history_action.setShortcut("Ctrl+H")
        history_action.setStatusTip("See the history of requests and responses")
        history_action.triggered.connect(lambda l: self.history_window.init_history_window())
        history_menu.addAction(history_action)
        menu_bar.addMenu(history_menu)

        additional_options_stacked_widget, select_operation_combo_box = \
            left_side_request_options_init(self.left_layout)

        # Submit buttton and it's functionality
        button_submit = QPushButton("Submit")
        button_submit.setStyleSheet("background-color: green")
        button_submit.setFont(font)
        button_submit.sizeHint()
        self.left_layout.addWidget(button_submit)

        button_submit.clicked.connect(lambda c:
                                      self.send_request_data_and_get_response(
                                          additional_options_stacked_widget.currentIndex(),
                                          additional_options_stacked_widget.currentWidget()))

        middle_response_init(self.middle_layout, self.state_dict, True)
        response_stacked_widget = QStackedWidget()
        select_operation_combo_box.activated[int].connect(response_stacked_widget.setCurrentIndex)

        left_vertical_line = QFrame()
        left_vertical_line.setFixedWidth(20)
        left_vertical_line.setFrameShape(QFrame.VLine)
        left_vertical_line.setFrameShadow(QFrame.Sunken)
        left_vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        left_vertical_line.setMinimumHeight(300)

        lower_box = self.current_state_window.init_current_state_window(font)

        left_size_constraint_widget = QWidget()
        left_size_constraint_widget.setMaximumWidth(600)
        left_size_constraint_widget.setMaximumHeight(400)
        left_size_constraint_widget.setLayout(self.left_layout)
        self.upper_layout.addWidget(left_size_constraint_widget)
        self.upper_layout.addWidget(left_vertical_line)

        middle_size_constraint_widget = QWidget()
        middle_size_constraint_widget.setMaximumWidth(600)
        middle_size_constraint_widget.setMaximumHeight(400)
        middle_size_constraint_widget.setLayout(self.middle_layout)
        self.upper_layout.addWidget(middle_size_constraint_widget)

        right_vertical_line = QFrame()
        right_vertical_line.setFixedWidth(20)
        right_vertical_line.setFrameShape(QFrame.VLine)
        right_vertical_line.setFrameShadow(QFrame.Sunken)
        right_vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        right_vertical_line.setMinimumHeight(300)
        self.upper_layout.addWidget(right_vertical_line)

        right_side_init(self.right_layout)
        self.upper_layout.addLayout(self.right_layout)

        self.upper_layout.addStretch()



        self.parent_layout.addLayout(self.upper_layout)
        self.parent_layout.addWidget(lower_box)
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

        middle_response_init(self.middle_layout, self.state_dict, False)
