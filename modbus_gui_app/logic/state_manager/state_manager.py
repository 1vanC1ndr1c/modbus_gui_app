from PySide2.QtCore import Signal, QObject

from modbus_gui_app.logic.state_manager import state_manager_functions


class StateManager(QObject):
    response_signal = Signal(bool)

    def __init__(self, gui_request_queue, database):
        super().__init__()
        self.last_ten_dicts = dict()
        self.database = database
        self.gui_request_queue = gui_request_queue
        self.modbus_connection = None
        self.current_request_and_response_dictionary = state_manager_functions.init_state()
        self.gui = None
        self.historian_db_current_index = 0
        self.historian_db_dicts = dict()
        self.current_coil_input_reg_states = state_manager_functions.init_current_states()

    # getters
    @property
    def request_and_response_state(self):
        return self.current_request_and_response_dictionary

    def get_last_ten_dicts(self):
        return self.last_ten_dicts

    def get_historian_db_dicts(self):
        self.state_manager_read_from_db()
        return self.historian_db_dicts

    # setters
    def set_gui(self, gui):
        self.gui = gui

    def set_current_request_serialized(self, current_request_serialized):
        self.current_request_and_response_dictionary["current_request_serialized"] = current_request_serialized

    def set_current_response_serialized(self, current_response_serialized):
        self.current_request_and_response_dictionary["current_response_serialized"] = current_response_serialized

    def set_current_unit_address(self, unit_address):
        self.current_request_and_response_dictionary["current_unit_address"] = unit_address

    def set_current_function_code(self, function_code):
        self.current_request_and_response_dictionary["current_function_code"] = function_code

    def set_current_request_name(self, req_name):
        self.current_request_and_response_dictionary["current_request_name"] = req_name

    def set_db_dicts(self, data):
        self.historian_db_dicts = data

    # connect to modbus
    def start_communications_thread(self):
        state_manager_functions.start_communications_thread(self)

    # user communication
    async def gui_to_state_manager_write(self):
        await state_manager_functions.gui_to_state_manager_write(self)

    async def send_request_to_modbus(self, valid_gui_request):
        await state_manager_functions.send_request_to_modbus(self, valid_gui_request)

    def process_modbus_response(self, deserialized_dict):
        state_manager_functions.process_modbus_response(self, deserialized_dict)

    # internal data and database
    def update_history_last_ten(self):
        state_manager_functions.update_history_last_ten(self)

    def state_manager_write_to_db(self):
        state_manager_functions.state_manager_write_to_db(self)

    def state_manager_read_from_db(self):
        state_manager_functions.state_manager_read_from_db(self)

    def reset_db_dict(self):
        state_manager_functions.reset_db_dict(self)

    # functions that deal with updating the current status in the lower part of the GUI.
    async def current_state_periodic_refresh(self):
        await state_manager_functions.current_state_periodic_refresh(self)

    def set_currently_selected_function(self):
        state_manager_functions.set_currently_selected_function(self)

    def update_current_coils_state(self):
        state_manager_functions.update_current_coils_state(self)
