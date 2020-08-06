import sys

from PySide2 import QtCore
from PySide2.QtGui import QFont, QIcon, Qt, QCloseEvent
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout, QSizePolicy, QFrame, QMenu, QMainWindow, QAction, QGroupBox

from modbus_gui_app.gui.current_state_window import CurrentStateWindow
from modbus_gui_app.gui.error_window import _init_error_window
from modbus_gui_app.gui.gui_left_side import _left_side_request_options_init
from modbus_gui_app.gui.gui_middle import _middle_init
from modbus_gui_app.gui.gui_right_side import ConnectionInfo
from modbus_gui_app.gui.history_window import HistoryWindow
from modbus_gui_app.gui import request_validation


def run_gui(state_manager):
    app = init_q_application()
    gui = Gui(state_manager)
    gui.setGeometry(100, 100, 900, 400)
    gui.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
    gui.showMaximized()
    app.exec_()


class Gui(QMainWindow):

    def __init__(self, state_manager):
        super().__init__()
        self._state_manager = state_manager
        self._state_manager.response_signal.connect(self._update_response_layout)
        self._state_manager.periodic_update_signal.connect(self._update_current_state_window)
        self._state_manager.invalid_connection_signal.connect(self._generate_invalid_connection_error)
        self._state_dict = state_manager.user_action_state
        self.gui_request_queue = state_manager.gui_request_queue
        self._state_manager.gui = self
        self._main_widget = QWidget()
        self._parent_layout = QVBoxLayout()
        self._upper_layout = QHBoxLayout()
        self._left_layout = QVBoxLayout()
        self._middle_layout = QVBoxLayout()
        self._right_layout = QVBoxLayout()
        self._history_window = HistoryWindow(state_manager)
        self._current_state_window = CurrentStateWindow(self, state_manager)

        self._font = QFont("Arial", 12)
        self._main_widget.setFont(self._font)

        self._menu_bar = self.menuBar()
        self._history_menu = QMenu("History")
        self._history_action = QAction("Open Request and Response History")
        self._history_action.setShortcut("Ctrl+H")
        self._history_action.setStatusTip("See the history of requests and responses")
        self._history_action.triggered.connect(lambda l: self._history_window.init_history_window())
        self._history_menu.addAction(self._history_action)
        self._menu_bar.addMenu(self._history_menu)

        self._left_side_parent_widget, self._left_side_options_stacked_widget, self.left_side_select_operation_box = \
            _left_side_request_options_init(self._left_layout)
        self._upper_layout.addWidget(self._left_side_parent_widget, 0, QtCore.Qt.AlignTop)

        self._left_vertical_line = self._create_vertical_line()
        self._upper_layout.addWidget(self._left_vertical_line)

        _middle_init(self._middle_layout, self._state_dict, True)
        self._middle_constraint_widget = QWidget()
        self._middle_constraint_widget.setMaximumWidth(600)
        self._middle_constraint_widget.setMaximumHeight(300)
        self._middle_constraint_widget.setLayout(self._middle_layout)
        self._upper_layout.addWidget(self._middle_constraint_widget, 0, QtCore.Qt.AlignTop)

        self._right_vertical_line = self._create_vertical_line()
        self._upper_layout.addWidget(self._right_vertical_line)

        self._connection_info = ConnectionInfo(self, self._state_manager)
        self._connection_info.right_side_init(self._right_layout)
        self._state_manager.connection_info_signal.connect(self._connection_info.generate_connection_info)
        self._upper_layout.addLayout(self._right_layout)

        self._button_submit = QPushButton("Submit")
        self._button_submit.setStyleSheet("background-color: green")
        self._button_submit.setFont(self._font)
        self._button_submit.sizeHint()
        self._button_submit.clicked.connect(lambda c:
                                            self._button_send_data(
                                                self._left_side_options_stacked_widget.currentIndex(),
                                                self._left_side_options_stacked_widget.currentWidget()))
        self._left_layout.addWidget(self._button_submit)
        self._left_layout.addStretch()
        self._parent_layout.addLayout(self._upper_layout)

        self._lower_box = QGroupBox()
        self._current_state_window.init_current_state_window()
        self.left_side_select_operation_box.currentIndexChanged.connect(
            self._current_state_window.signal_current_state_window_from_gui)
        self._parent_layout.addWidget(self._lower_box)

        self._main_widget.setLayout(self._parent_layout)
        self.setCentralWidget(self._main_widget)

    def _button_send_data(self, index, stacked_widget):
        function_code = index + 1
        is_valid, validation_result = request_validation.get_request_validation_result(function_code, stacked_widget)

        if is_valid is True:
            self.gui_request_queue.put(validation_result)

        elif is_valid is False:
            _init_error_window(validation_result)

    def _update_response_layout(self, flag):
        _middle_init(self._middle_layout, self._state_dict, flag)

    def _update_current_state_window(self, is_first):
        self._current_state_window.signal_current_state_window_from_state_manager(is_first)

    def _create_vertical_line(self):
        vertical_line = QFrame()
        vertical_line.setFixedWidth(20)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        vertical_line.setMinimumHeight(300)
        return vertical_line

    def _generate_invalid_connection_error(self):
        _init_error_window("No Connection Established.")

    def closeEvent(self, event: QCloseEvent):
        try:
            self._state_manager.ws_read_loop_future.cancel()
        except Exception as close_exception:
            print("WINDOW: Error When Closing The App: ", close_exception)
        try:
            self._state_manager.database.db_close()
        except Exception as close_exception:
            print("WINDOW: Error When Closing The App: ", close_exception)
        self._state_manager.gui_request_queue.put("End.")
        event.accept()


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
