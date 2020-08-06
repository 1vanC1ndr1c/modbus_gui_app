from PySide2 import QtCore
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PySide2.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QHeaderView, QAbstractItemView


class HistoryWindow:

    def __init__(self, state_manager):
        self._state_manager = state_manager
        self._is_first = True
        self._more_data = []
        self._last_ten_dicts = []
        self._rows = None
        self._table_view = None

    def init_history_window(self):
        self._rows = QStandardItemModel()
        self._is_first = True
        self._last_ten_dicts = self._state_manager.last_ten_dicts

        history_dlg_window = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        history_dlg_window.setWindowIcon(QIcon("resources/history_icon.png"))
        history_dlg_window.setMinimumHeight(500)
        history_dlg_window.setMinimumWidth(1600)
        history_dlg_window.setWindowTitle("HISTORY")
        history_parent_layout = QVBoxLayout()

        self._table_view = QTableView()
        self._table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_view.horizontalHeader().setStretchLastSection(True)
        self._table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self._rows.setHorizontalHeaderLabels([
            "TIME STAMP",
            "TID",
            "TYPE",
            "NAME",
            "VALID",
            "ERROR MESSAGE",
            "UNIT ADDRESS",
            "FUNCTION CODE",
            "SERIALIZED BYTE DATA"
        ])

        self._table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self._table_view.setModel(self._rows)
        history_parent_layout.addWidget(self._table_view)

        if len(self._last_ten_dicts) == 0:
            no_data_list = []
            for i in range(0, 9):
                no_data_list.append(QStandardItem("No Data..."))
            self._rows.appendRow(no_data_list)

        else:
            self._set_history_data(self._last_ten_dicts)

        button_submit = QPushButton()
        button_submit.setText("More")
        button_submit.setStyleSheet("background-color: green")
        button_submit.sizeHint()
        button_font = QFont("Arial", 11)
        button_submit.setFont(button_font)
        history_parent_layout.addWidget(button_submit)

        button_submit.clicked.connect(lambda c: self._get_more_data(self._state_manager))

        history_dlg_window.setLayout(history_parent_layout)
        history_dlg_window.exec_()

    def _set_history_data(self, history_dict):
        for dct in history_dict:
            current_dict = history_dict[dct]

            req_time_stamp = QStandardItem(str(current_dict["current_request_sent_time"]))
            tid_req = QStandardItem(str(current_dict["current_tid"]))
            req_type = QStandardItem("Request.")
            req_validity = QStandardItem(str(current_dict["current_request_from_gui_is_valid"]))
            req_f_code_name = QStandardItem(str(current_dict["current_request_name"]))
            req_err_msg = QStandardItem(str(current_dict["current_request_from_gui_error_msg"]))
            req_unit_address = QStandardItem(str(current_dict["current_unit_address"]))
            req_f_code = QStandardItem(str(current_dict["current_function_code"]))
            req_byte = _split_bytes_into_rows_of_three(current_dict["current_request_serialized"])

            resp_time_stamp = QStandardItem(str(current_dict["current_response_received_time"]))
            tid_resp = QStandardItem(str(current_dict["current_tid"]))
            resp_type = QStandardItem("Response.")
            resp_validity = QStandardItem(str(current_dict["current_response_is_valid"]))
            resp_f_code_name = QStandardItem(str(current_dict["current_request_name"]))
            resp_err_msg = QStandardItem(str(current_dict["current_response_err_msg"]))
            resp_unit_address = QStandardItem(str(current_dict["current_unit_address"]))
            resp_f_code = QStandardItem(str(current_dict["current_function_code"]))
            resp_byte = _split_bytes_into_rows_of_three(current_dict["current_response_serialized"])

            req_data_list = [req_time_stamp, tid_req, req_type, req_f_code_name, req_validity, req_err_msg,
                             req_unit_address, req_f_code, req_byte]
            resp_data_list = [resp_time_stamp, tid_resp, resp_type, resp_f_code_name, resp_validity, resp_err_msg,
                              resp_unit_address, resp_f_code, resp_byte]
            self._rows.appendRow(req_data_list)
            self._rows.appendRow(resp_data_list)
            self._table_view.resizeRowsToContents()

    def _get_more_data(self, state_manager):
        if self._is_first is True:
            self._is_first = False
            state_manager.reset_db_dict()
            self._rows.removeRow(0)

        self._more_data = state_manager.get_historian_db_dicts()
        self._set_history_data(self._more_data)


def _split_bytes_into_rows_of_three(data):
    data = str(data)
    data = data.split("\\")
    r_tmp = data
    for i in range(3, len(data) + 4, 4):
        r_tmp[i:i] = "\n"
    data = r_tmp

    return QStandardItem("".join(data))
