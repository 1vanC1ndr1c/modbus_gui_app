import sys

from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, \
    QHBoxLayout, QSizePolicy, QFrame, QMenu, QMainWindow, QAction, QLabel
from PySide2.QtGui import QFont, QIcon
from PySide2 import QtCore

from modbus_gui_app.gui.gui_left_side import left_side_request_options_init

from modbus_gui_app.gui.current_state_window import CurrentStateWindow
from modbus_gui_app.gui.gui_right_side import right_side_init
from modbus_gui_app.gui.error_window import init_error_window
from modbus_gui_app.gui.history_window import HistoryWindow
from modbus_gui_app.gui.gui_middle import middle_init

from modbus_gui_app.logic import validation


def run_gui(state_manager, gui_request_queue):
    app = init_q_application()
    gui = Gui(state_manager, gui_request_queue)
    gui.setGeometry(100, 100, 900, 400)
    gui.show()
    sys.exit(app.exec_())


class Gui(QMainWindow):

    def __init__(self, state_manager, gui_request_queue):
        super().__init__()
        self.state_manager = state_manager
        self.state_manager.response_signal.connect(self.update_response_layout)
        self.state_dict = state_manager.current_request_and_response_dictionary
        self.gui_request_queue = gui_request_queue
        self.state_manager.set_gui(self)

        self.main_widget = QWidget()
        self.parent_layout = QVBoxLayout()
        self.upper_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.history_window = HistoryWindow(state_manager)
        self.current_state_window = CurrentStateWindow(state_manager)

        self.font = QFont("Arial", 12)
        self.main_widget.setFont(self.font)
        self.parent_layout.setStretchFactor(self.left_layout, 0)
        self.parent_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.menu_bar = self.menuBar()
        self.history_menu = QMenu("History")
        self.history_action = QAction("Open Request and Response History")
        self.history_action.setShortcut("Ctrl+H")
        self.history_action.setStatusTip("See the history of requests and responses")
        self.history_action.triggered.connect(lambda l: self.history_window.init_history_window())
        self.history_menu.addAction(self.history_action)

        self.menu_bar.addMenu(self.history_menu)

        self.left_side_parent_widget, self.left_side_options_stacked_widget, self.left_side_select_operation_box = \
            left_side_request_options_init(self.left_layout)
        self.upper_layout.addWidget(self.left_side_parent_widget)

        self.left_vertical_line = self.create_vertical_line()
        self.upper_layout.addWidget(self.left_vertical_line)

        middle_init(self.middle_layout, self.state_dict, True)
        self.middle_constraint_widget = QWidget()
        self.middle_constraint_widget.setMaximumWidth(600)
        self.middle_constraint_widget.setMaximumHeight(300)
        self.middle_constraint_widget.setLayout(self.middle_layout)
        self.upper_layout.addWidget(self.middle_constraint_widget)

        self.right_vertical_line = self.create_vertical_line()
        self.upper_layout.addWidget(self.right_vertical_line)

        right_side_init(self.right_layout)
        self.upper_layout.addLayout(self.right_layout)

        self.button_submit = QPushButton("Submit")
        self.button_submit.setStyleSheet("background-color: green")
        self.button_submit.setFont(self.font)
        self.button_submit.sizeHint()
        self.button_submit.clicked.connect(lambda c:
                                           self.button_send_request_data(
                                               self.left_side_options_stacked_widget.currentIndex(),
                                               self.left_side_options_stacked_widget.currentWidget()))
        self.left_layout.addWidget(self.button_submit)

        self.parent_layout.addLayout(self.upper_layout)

        self.lower_box = self.update_current_state_window()

        self.parent_layout.addWidget(self.lower_box)

        self.main_widget.setLayout(self.parent_layout)
        self.setCentralWidget(self.main_widget)

    def button_send_request_data(self, index, stacked_widget):
        function_code = index + 1
        is_valid, validation_result = validation.get_request_validation_result(function_code, stacked_widget)

        if is_valid is True:
            self.gui_request_queue.put(validation_result)

        elif is_valid is False:
            init_error_window(validation_result)

    def update_response_layout(self, flag):
        middle_init(self.middle_layout, self.state_dict, flag)
        self.update_current_state_window()

    def update_current_state_window(self):
        return self.current_state_window.init_current_state_window(self.font, self.left_side_select_operation_box)

    def create_vertical_line(self):
        vertical_line = QFrame()
        vertical_line.setFixedWidth(20)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        vertical_line.setMinimumHeight(300)
        return vertical_line


def init_q_application():
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
