from PySide2.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QAbstractScrollArea, QHeaderView, \
    QAbstractItemView
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide2 import QtCore, QtGui

from modbus_gui_app.logic.state_manager import StateManager


def init_history_window(state_manager):
    history_dlg_window = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
    history_dlg_window.setMinimumHeight(500)
    history_dlg_window.setMinimumWidth(1600)
    history_dlg_window.setWindowTitle("HISTORY")
    history_parent_layout = QVBoxLayout()

    table_view = QTableView()
    table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table_view.horizontalHeader().setStretchLastSection(True)
    table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

    names = QStandardItemModel()
    names.setHorizontalHeaderLabels(["TIME STAMP",
                                     "TID",
                                     "TYPE",
                                     "NAME",
                                     "VALID",
                                     "ERROR MESSAGE",
                                     "UNIT ADDRESS",
                                     "FUNCTION CODE",
                                     "SERIALIZED BYTE DATA"])

    table_view.setStyleSheet("QHeaderView::section { background-color:lightgray }")
    table_view.setModel(names)
    history_parent_layout.addWidget(table_view)

    last_ten_dicts = state_manager.get_last_ten_dicts()

    if len(last_ten_dicts) == 0:
        no_data_list = []
        for i in range(0, 9):
            no_data_list.append(QStandardItem("No Data..."))
        names.appendRow(no_data_list)

    else:
        for dct in last_ten_dicts:
            current_dict = last_ten_dicts[dct]

            req_time_stamp = QStandardItem(str(current_dict["current_request_sent"]))
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

            names.appendRow(req_data_list)

            resp_time_stamp = QStandardItem(str(current_dict["current_response_received"]))
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

            names.appendRow(resp_data_list)

    table_view.resizeRowsToContents()

    button_submit = QPushButton()
    button_submit.setText("Get 10 More")
    button_submit.setStyleSheet("background-color: green")
    button_submit.sizeHint()
    button_font = QFont("Arial", 11)
    button_submit.setFont(button_font)
    history_parent_layout.addWidget(button_submit)

    button_submit.clicked.connect(lambda c: get_more_data(state_manager))

    history_dlg_window.setLayout(history_parent_layout)
    history_dlg_window.exec_()


def get_more_data(state_manager):
    db_dict = {}
    # TODO connect to state_manager to get 10 more inputs from db and show them in the hist. dlg. window


def split_bytes_into_rows_of_three(data):
    data = str(data)
    data = data.split("\\")
    r_tmp = data
    for i in range(3, len(data) + 4, 4):
        r_tmp[i:i] = "\n"
    data = r_tmp

    return QStandardItem("".join(data))
