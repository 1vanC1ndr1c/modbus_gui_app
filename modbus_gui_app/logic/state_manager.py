from modbus_gui_app.logic.validation import get_validation_result
from datetime import datetime
from copy import deepcopy


class StateManager:
    def __init__(self, modbus_request_queue, modbus_response_queue):
        self.modbus_request_queue = modbus_request_queue
        self.modbus_response_queue = modbus_response_queue
        self.last_ten_dicts = {}

    gui = None
    current_state_dict = {
        "current_tid": 0,
        "current_unit_address": "00",
        "current_function_code": "00",
        "current_request_name": "Unknown Request.",
        "current_request_from_gui": '/',
        "current_request_from_gui_is_valid": False,
        "current_request_from_gui_error_msg": "/",
        "current_request_serialized": b'0',
        "current_request_sent": 0,
        "current_response_received": 0,
        "current_response_serialized": b'0',
        "current_response_is_valid": False,
        "current_response_err_msg": "/",
        "current_response_returned_values": "/",
    }

    # setters
    def set_gui(self, gui):
        self.gui = gui

    def set_current_tid(self):
        tid = self.current_state_dict.get("current_tid")
        if tid > 9999:
            tid = 0
        else:
            tid = tid + 1
        self.current_state_dict["current_tid"] = tid

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

    # getters
    def get_dict(self):
        return self.current_state_dict

    def get_last_ten_dicts(self):
        return self.last_ten_dicts

    # communication
    def send_request(self, index, widget):
        function_code = index + 1
        is_valid, validation_result = get_validation_result(function_code, widget)  # validate gui request data

        if is_valid is True:
            # send the validated data(in a dict) to COMM
            self.set_current_tid()
            self.current_state_dict["current_request_from_gui"] = validation_result
            self.current_state_dict["current_request_from_gui_is_valid"] = True
            self.current_state_dict["current_request_from_gui_error_msg"] = "/"
            self.current_state_dict["current_request_sent"] = datetime.now()
            self.modbus_request_queue.put(self.current_state_dict)
        else:
            # data is invalid, inform the GUI, set dict values
            self.set_current_tid()
            self.current_state_dict["current_request_from_gui"] = "/"
            self.current_state_dict["current_request_from_gui_is_valid"] = False
            self.current_state_dict["current_request_from_gui_error_msg"] = validation_result
            self.current_state_dict["current_response_serialized"] = "/"
            self.current_state_dict["current_request_sent"] = datetime.now()
            self.set_current_request_serialized('/')
            self.set_current_response_serialized('/')

    def get_response(self):
        try:
            # TODO fix this somehow, don't like it
            deserialized_dict = self.modbus_response_queue.get(block=True)
        except:
            deserialized_dict = "/"
        self.current_state_dict["current_response_received"] = datetime.now()
        if deserialized_dict != "/":
            for key in deserialized_dict:
                if key in self.current_state_dict:
                    self.current_state_dict[key] = deserialized_dict[key]

        self.update_history_last_ten()

    def update_history_last_ten(self):
        # save only the last 10. If more, delete the oldest one.
        if len(self.last_ten_dicts) >= 10:
            min_key = min(self.last_ten_dicts.keys())
            self.last_ten_dicts.pop(min_key)

        # use deepcopy, otherwise, the older data will be overwritten
        tid = deepcopy(self.current_state_dict["current_tid"])
        self.last_ten_dicts[tid] = deepcopy(self.current_state_dict)

    def write_to_db(self):
        # TODO save the current dict into the db
        return

    def stm_read_from_db(self, start_index, no_of_elements):
        # TODO read from db

        # the data will be stored in a list of dictionaries
        db_dict_list = []

        return db_dict_list
