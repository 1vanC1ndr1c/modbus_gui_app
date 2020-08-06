from PySide2.QtCore import Signal, QObject

from modbus_gui_app.logic.state import state_manager_functions
from modbus_gui_app.logic.state import state_manager_live_update
from modbus_gui_app.database.db_handler import Backend

import queue


class StateManager(QObject):
    response_signal = Signal(bool)
    periodic_update_signal = Signal(bool)
    connection_info_signal = Signal(str)
    invalid_connection_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.last_ten_dicts = {}
        self.database = Backend()
        self.database.set_st_manager(self)
        self.gui_request_queue = queue.Queue()
        self.modbus_connection = None
        self.user_action_state = state_manager_functions.init_state()
        self.gui = None
        self.historian_db_current_index = 0
        self.historian_db_dicts = {}
        self.live_update_states = state_manager_live_update.init_live_update_states()
        self.current_state_periodic_refresh_future = None

    def get_historian_db_dicts(self):
        self.state_manager_read_from_db()
        return self.historian_db_dicts


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
        await state_manager_live_update.current_state_periodic_refresh(self)

    def set_currently_selected_function(self, source):
        state_manager_live_update.set_currently_selected_automatic_request(self, source)

    def update_current_coils_state(self, source):
        state_manager_live_update.update_current_coils_state(self, source)
