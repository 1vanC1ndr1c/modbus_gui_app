from modbus_gui_app.logic.validation import get_validation_result
from datetime import datetime
from copy import deepcopy


class StateManager:
    def __init__(self, modbus_request_queue, modbus_response_queue,
                 db_read_queue_request, db_read_queue_response, db_write_queue):
        self.modbus_request_queue = modbus_request_queue
        self.modbus_response_queue = modbus_response_queue
        self.last_ten_dicts = {}
        self.db_read_queue_request = db_read_queue_request
        self.db_read_queue_response = db_read_queue_response
        self.db_write_queue = db_write_queue

    gui = None
    current_state_dict = {
        "current_tid": 0,
        "current_unit_address": "00",
        "current_function_code": "00",
        "current_request_name": "Unknown Request.",
        "current_request_from_gui": '-',
        "current_request_from_gui_is_valid": False,
        "current_request_from_gui_error_msg": "-",
        "current_request_serialized": b'0',
        "current_request_sent_time": 0,
        "current_response_received_time": 0,
        "current_response_serialized": b'0',
        "current_response_is_valid": False,
        "current_response_err_msg": "-",
        "current_response_returned_values": "-",
    }

    db_current_index = 0
    db_dicts = {}

    # setters
    def set_gui(self, gui):
        self.gui = gui

    def set_current_request_serialized(self, current_request_serialized):
        self.current_state_dict["current_request_serialized"] = current_request_serialized

    def set_current_response_serialized(self, current_response_serialized):
        self.current_state_dict["current_response_serialized"] = current_response_serialized

    def set_current_unit_address(self, unit_address):
        self.current_state_dict["current_unit_address"] = unit_address

    def set_current_function_code(self, function_code):
        self.current_state_dict["current_function_code"] = function_code

    def set_current_request_name(self, req_name):
        self.current_state_dict["current_request_name"] = req_name

    def set_db_dicts(self, data):
        self.db_dicts = data

    # getters
    def get_dict(self):
        return self.current_state_dict

    def get_last_ten_dicts(self):
        return self.last_ten_dicts

    def get_db_dicts(self):
        self.state_manager_read_from_db()
        return self.db_dicts

    # communication
    def send_request(self, index, widget):
        function_code = index + 1
        is_valid, validation_result = get_validation_result(function_code, widget)  # validate gui request data

        if is_valid is True:
            # send the validated data(in a dict) to COMM
            #self.set_current_tid()
            self.current_state_dict["current_request_from_gui"] = validation_result
            self.current_state_dict["current_request_from_gui_is_valid"] = True
            self.current_state_dict["current_request_from_gui_error_msg"] = "-"
            self.current_state_dict["current_request_sent_time"] = datetime.now()
            self.modbus_request_queue.put(self.current_state_dict)
        # else:
        #     # data is invalid, inform the GUI, set dict values
        #     self.set_current_tid()
        #     self.current_state_dict["current_request_from_gui"] = "-"
        #     self.current_state_dict["current_request_from_gui_is_valid"] = False
        #     self.current_state_dict["current_request_from_gui_error_msg"] = validation_result
        #     self.current_state_dict["current_response_serialized"] = "-"
        #     self.current_state_dict["current_request_sent_time"] = datetime.now()
        #     self.set_current_request_serialized('/')
        #     self.set_current_response_serialized('/')

    def get_response(self):
        try:
            # TODO fix this somehow, don't like it
            deserialized_dict = self.modbus_response_queue.get(block=True, timeout=5)
        except:
            deserialized_dict = "-"
            self.current_state_dict["current_response_err_msg"] = "No Response Received."
        self.current_state_dict["current_response_received_time"] = datetime.now()
        if deserialized_dict != "-":
            for key in deserialized_dict:
                if key in self.current_state_dict:
                    self.current_state_dict[key] = deserialized_dict[key]
        # dictionary housekeeping
        self.update_history_last_ten()
        self.state_manager_write_to_db()

    # internal data and database

    def update_history_last_ten(self):
        # save only the last 10. If more, delete the oldest one.
        if len(self.last_ten_dicts) >= 10:
            min_key = min(self.last_ten_dicts.keys())
            self.last_ten_dicts.pop(min_key)
        # use deepcopy, otherwise, the older data will be overwritten
        tid = deepcopy(self.current_state_dict["current_tid"])
        self.last_ten_dicts[tid] = deepcopy(self.current_state_dict)

    def state_manager_write_to_db(self):
        self.db_write_queue.put(self.current_state_dict)
        return

    def state_manager_read_from_db(self):
        self.db_read_queue_request.put(["READ FROM DB", self.db_current_index])
        self.db_read_queue_response.get()  # wait for the response
        self.db_current_index = self.db_current_index + 10

    def reset_db_dict(self):
        self.db_dicts = {}
        self.db_current_index = 0
