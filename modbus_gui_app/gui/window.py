import sys

from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, \
    QHBoxLayout, QSizePolicy, QFrame, QMenu, QMainWindow, QAction
from PySide2.QtGui import QFont, QIcon
from PySide2 import QtCore

from modbus_gui_app.gui.gui_left_side import left_side_request_options_init
from modbus_gui_app.gui.gui_middle import middle_init, init_error_window
from modbus_gui_app.gui.current_state_window import CurrentStateWindow
from modbus_gui_app.gui.gui_right_side import right_side_init
from modbus_gui_app.gui.history_window import HistoryWindow
from modbus_gui_app.logic import validation


def start_app(state_manager, gui_request_queue):
    gui = Gui(state_manager, gui_request_queue)
    gui.init_gui()


class Gui:
    def __init__(self, state_manager, gui_request_queue):
        self.state_manager = state_manager
        self.state_dict = state_manager.current_req_resp_dict
        self.left_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.parent_layout = QVBoxLayout()
        self.upper_layout = QHBoxLayout()
        self.history_window = HistoryWindow(state_manager)
        self.current_state_window = CurrentStateWindow(state_manager)
        self.gui_request_queue = gui_request_queue

    def init_gui(self):

        app = self.init_q_application()

        window = QMainWindow()
        # window.setGeometry(100, 100, 1800, 900)
        window.setGeometry(100, 100, 900, 400)

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

        left_side_parent_widget, left_side_options_stacked_widget, left_side_select_operation_box = \
            left_side_request_options_init(self.left_layout)
        self.upper_layout.addWidget(left_side_parent_widget)

        left_vertical_line = self.create_vertical_line()
        self.upper_layout.addWidget(left_vertical_line)

        middle_init(self.middle_layout, self.state_dict, True)
        response_stacked_widget = QStackedWidget()
        left_side_select_operation_box.activated[int].connect(response_stacked_widget.setCurrentIndex)
        middle_constraint_widget = QWidget()
        middle_constraint_widget.setMaximumWidth(600)
        middle_constraint_widget.setMaximumHeight(300)
        middle_constraint_widget.setLayout(self.middle_layout)
        self.upper_layout.addWidget(middle_constraint_widget)

        right_vertical_line = self.create_vertical_line()
        self.upper_layout.addWidget(right_vertical_line)

        right_side_init(self.right_layout)
        self.upper_layout.addLayout(self.right_layout)

        button_submit = QPushButton("Submit")
        button_submit.setStyleSheet("background-color: green")
        button_submit.setFont(font)
        button_submit.sizeHint()
        button_submit.clicked.connect(lambda c:
                                      self.button_send_request_data(
                                          left_side_options_stacked_widget.currentIndex(),
                                          left_side_options_stacked_widget.currentWidget()))
        self.left_layout.addWidget(button_submit)

        self.parent_layout.addLayout(self.upper_layout)

        # lower_box = self.current_state_window.init_current_state_window(font)
        # self.parent_layout.addWidget(lower_box)

        main_widget.setLayout(self.parent_layout)
        window.setCentralWidget(main_widget)
        window.show()
        app.exec_()

    def button_send_request_data(self, index, stacked_widget):
        function_code = index + 1
        is_valid, validation_result = validation.get_validation_result(function_code, stacked_widget)

        if is_valid is True:
            self.gui_request_queue.put(validation_result)

        elif is_valid is False:
            init_error_window(validation_result)

        middle_init(self.middle_layout, self.state_dict, False)

    def update_response(self):
        return
    # self.state_manager.response_signal.connect(self.update_response())

    def init_q_application(self):
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
        return app

    def create_vertical_line(self):
        vertical_line = QFrame()
        vertical_line.setFixedWidth(20)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        vertical_line.setMinimumHeight(300)
        return vertical_line
