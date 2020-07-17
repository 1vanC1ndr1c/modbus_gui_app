from modbus_gui_app.logic.validation import get_validation_result


class StateManager:
    def __init__(self, modbus_request_queue, modbus_response_queue):
        self.modbus_request_queue = modbus_request_queue
        self.modbus_response_queue = modbus_response_queue

    # "request_history": "todo A DICT WITH TID AS A KEY",
    # "response_history": "todo A DICT WITH TID AS A KEY",
    # "TODO": "other stuff"
    gui = None
    state_dict = {
        "current_tid": 0,
        "current_request_from_gui": '',
        "current_request_from_gui_is_valid": False,
        "current_request_from_gui_error_msg": "",
        "current_request_serialized": b'0',
        "current_response_serialized": b'0',
        "current_response_is_valid": False,
        "current_response_err_msg": "",
        "current_response_returned_values": "",
    }
    # format: "TID", ["request msg", "valid/invalid", "err_msg"]
    request_history_dict = {}
    # format: "TID", ["response msg", "valid/invalid", "err_msg"]
    response_history_dict = {}

    # setters
    def set_gui(self, gui):
        self.gui = gui

    def set_current_tid(self):
        tid = self.state_dict.get("current_tid")
        if tid > 9999:
            tid = 0
        else:
            tid = tid + 1
        self.state_dict["current_tid"] = tid

    def set_current_request_serialized(self, current_request_serialized):
        self.state_dict["current_request_serialized"] = current_request_serialized

    def set_current_response_serialized(self, current_response_serialized):
        self.state_dict["current_response_serialized"] = current_response_serialized

    # getters
    def get_dict(self):
        return self.state_dict

    # communication
    def send_request(self, index, widget):
        function_code = index + 1
        is_valid, validation_result = get_validation_result(function_code, widget)  # validate gui request data

        if is_valid is True:
            # send the validated data(in a dict) to COMM
            self.set_current_tid()
            self.state_dict["current_request_from_gui"] = validation_result
            self.state_dict["current_request_from_gui_is_valid"] = True
            self.state_dict["current_request_from_gui_error_msg"] = "/"
            self.modbus_request_queue.put(self.state_dict)
        else:
            # data is invalid, inform the GUI, set dict values
            self.set_current_tid()
            self.state_dict["current_request_from_gui"] = "/"
            self.state_dict["current_request_from_gui_is_valid"] = False
            self.state_dict["current_request_from_gui_error_msg"] = validation_result
            self.state_dict["current_response_serialized"] = "/"
            self.set_current_request_serialized('/')
            self.set_current_response_serialized('/')

    def get_response(self):
        try:
            deserialized_dict = self.modbus_response_queue.get(block=True, timeout=1.5)
        except:
            deserialized_dict = "/"

        if deserialized_dict != "/":
            for key in deserialized_dict:
                if key in self.state_dict:
                    self.state_dict[key] = deserialized_dict[key]


