from PySide2.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QHeaderView, QAbstractItemView
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont, QIcon
from PySide2 import QtCore


class HistoryWindow:

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.isFirst = True
        self.more_data = []
        self.last_ten_dicts = []
        self.rows = None
        self.table_view = None

    def init_history_window(self):
        self.rows = QStandardItemModel()
        self.isFirst = True
        self.last_ten_dicts = self.state_manager.get_last_ten_dicts()

        history_dlg_window = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        history_dlg_window.setWindowIcon(QIcon("resources/history_icon.png"))
        history_dlg_window.setMinimumHeight(500)
        history_dlg_window.setMinimumWidth(1600)
        history_dlg_window.setWindowTitle("HISTORY")
        history_parent_layout = QVBoxLayout()

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.rows.setHorizontalHeaderLabels(["TIME STAMP",
                                             "TID",
                                             "TYPE",
                                             "NAME",
                                             "VALID",
                                             "ERROR MESSAGE",
                                             "UNIT ADDRESS",
                                             "FUNCTION CODE",
                                             "SERIALIZED BYTE DATA"])

        self.table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
        self.table_view.setModel(self.rows)
        history_parent_layout.addWidget(self.table_view)

        if len(self.last_ten_dicts) == 0:
            no_data_list = []
            for i in range(0, 9):
                no_data_list.append(QStandardItem("No Data..."))
            self.rows.appendRow(no_data_list)

        else:
            self.set_history_data(self.last_ten_dicts)

        button_submit = QPushButton()
        button_submit.setText("More")
        button_submit.setStyleSheet("background-color: green")
        button_submit.sizeHint()
        button_font = QFont("Arial", 11)
        button_submit.setFont(button_font)
        history_parent_layout.addWidget(button_submit)

        button_submit.clicked.connect(lambda c: self.get_more_data(self.state_manager))

        history_dlg_window.setLayout(history_parent_layout)
        history_dlg_window.exec_()

    def set_history_data(self, history_dict):
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
            req_byte = split_bytes_into_rows_of_three(current_dict["current_request_serialized"])

            req_data_list = [req_time_stamp, tid_req, req_type, req_f_code_name, req_validity, req_err_msg,
                             req_unit_address, req_f_code, req_byte]

            self.rows.appendRow(req_data_list)

            resp_time_stamp = QStandardItem(str(current_dict["current_response_received_time"]))
            tid_resp = QStandardItem(str(current_dict["current_tid"]))
            resp_type = QStandardItem("Response.")
            resp_validity = QStandardItem(str(current_dict["current_response_is_valid"]))
            resp_f_code_name = QStandardItem(str(current_dict["current_request_name"]))
            resp_err_msg = QStandardItem(str(current_dict["current_response_err_msg"]))
            resp_unit_address = QStandardItem(str(current_dict["current_unit_address"]))
            resp_f_code = QStandardItem(str(current_dict["current_function_code"]))
            resp_byte = split_bytes_into_rows_of_three(current_dict["current_response_serialized"])

            resp_data_list = [resp_time_stamp, tid_resp, resp_type, resp_f_code_name, resp_validity, resp_err_msg,
                              resp_unit_address, resp_f_code, resp_byte]

            self.rows.appendRow(resp_data_list)
            self.table_view.resizeRowsToContents()

    def get_more_data(self, state_manager):
        if self.isFirst is True:
            self.isFirst = False
            state_manager.reset_db_dict()
            self.rows.removeRow(0)

        self.more_data = state_manager.get_db_dicts()
        self.set_history_data(self.more_data)


def split_bytes_into_rows_of_three(data):
    data = str(data)
    data = data.split("\\")
    r_tmp = data
    for i in range(3, len(data) + 4, 4):
        r_tmp[i:i] = "\n"
    data = r_tmp

    return QStandardItem("".join(data))
