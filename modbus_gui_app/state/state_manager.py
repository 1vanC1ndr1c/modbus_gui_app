import asyncio
import functools
import queue
from concurrent.futures.thread import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime
from threading import Thread

from PySide2.QtCore import Signal, QObject

from modbus_gui_app.communication.modbus_connection import ModbusConnection
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.state.state_manager_data_structures import _init_user_action_state_dict, \
    _init_live_update_states
from modbus_gui_app.state.state_manager_live_update import _live_update_loop, \
    _set_currently_selected_automatic_request

from modbus_gui_app.communication.user_request_serializer import read_coils_serialize2, read_discrete_inputs_serialize, \
    read_holding_registers_serialize, read_input_registers_serialize, write_single_coil_serialize, \
    write_single_register_serialize


class StateManager(QObject):
    response_signal = Signal(bool)
    periodic_update_signal = Signal(bool)
    connection_info_signal = Signal(str)
    invalid_connection_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.last_ten_dicts = {}
        self.database = Backend()
        self.gui_request_queue = queue.Queue()
        self.modbus_connection = None
        self.user_action_state = _init_user_action_state_dict()
        self.gui = None
        self._historian_db_current_index = 0
        self._historian_db_dicts = {}
        self.live_update_states = _init_live_update_states()
        self.ws_read_loop_future = None

    def get_historian_db_dicts(self):
        self._read_from_db()
        return self._historian_db_dicts

    def start_communications_thread(self):
        communications_thread = Thread(
            daemon=True,
            target=lambda: asyncio.new_event_loop().run_until_complete(
                self._start_readers_and_writers()))
        communications_thread.start()

    async def _start_readers_and_writers(self):
        self.modbus_connection = ModbusConnection()
        self.modbus_connection.live_update_states.update(self.live_update_states)
        await self.modbus_connection.open_session()
        self.connection_info_signal.emit("Connection Established")

        live_update_refresh_future = asyncio.ensure_future(_live_update_loop(self))
        ws_read_loop_future = asyncio.ensure_future(self.modbus_connection.ws_read_loop())
        self.ws_read_loop_future = ws_read_loop_future
        state_manager_to_modbus_write_future = asyncio.ensure_future(self.gui_queue_read_loop())

        await asyncio.wait([ws_read_loop_future, live_update_refresh_future, state_manager_to_modbus_write_future],
                           return_when=asyncio.FIRST_COMPLETED)

        state_manager_to_modbus_write_future.cancel()
        live_update_refresh_future.cancel()
        ws_read_loop_future.cancel()
        try:
            await self.modbus_connection.ws.close()
        except Exception as conn_error:
            print("STATE MANAGER FUNCTIONS: Error When Connecting, No Connection. ", conn_error)
            self.invalid_connection_signal.emit("No Connection.")
            self.connection_info_signal.emit("No Connection.")

        await self.modbus_connection.session.close()

    async def gui_queue_read_loop(self):
        executor = ThreadPoolExecutor(1)
        while True:
            gui_request_data = await asyncio.get_event_loop().run_in_executor(
                executor, functools.partial(self._get_msg_from_gui_queue))
            if gui_request_data == "End.":
                break
            await self._send_request_to_modbus(gui_request_data)

    def _get_msg_from_gui_queue(self):
        request = self.gui_request_queue.get()
        return request

    async def _send_request_to_modbus(self, gui_request_data):
        function_code = gui_request_data[-1]
        tid = self.modbus_connection.tid + 1
        start_addr = gui_request_data[0]
        unit_addr = gui_request_data[2]
        response = None

        if function_code == 1:
            no_of_coils = gui_request_data[1]
            bytes_reg, results_dict = read_coils_serialize2(start_addr, no_of_coils, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_read_coils(start_addr, no_of_coils, unit_addr)

        elif function_code == 2:
            input_count = gui_request_data[1]
            bytes_reg, results_dict = read_discrete_inputs_serialize(start_addr, input_count, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_read_discrete_inputs(start_addr, input_count, unit_addr)

        elif function_code == 3:
            h_regs_count = gui_request_data[1]
            bytes_reg, results_dict = read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_read_holding_registers(start_addr, h_regs_count, unit_addr)

        elif function_code == 4:
            in_regs_count = gui_request_data[1]
            bytes_reg, results_dict = read_input_registers_serialize(start_addr, in_regs_count, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_read_input_registers(start_addr, in_regs_count, unit_addr)

        elif function_code == 5:
            coil_state = gui_request_data[1]
            bytes_reg, results_dict = write_single_coil_serialize(start_addr, coil_state, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_write_single_coil(start_addr, coil_state, unit_addr)

        elif function_code == 6:
            reg_value = gui_request_data[1]
            bytes_reg, results_dict = write_single_register_serialize(start_addr, reg_value, unit_addr, tid)
            self.user_action_state.update(results_dict)
            self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_write_single_register(start_addr, reg_value, unit_addr)

        if response is not None:
            self.user_action_state.update(self.modbus_connection.communication_dict)
            self._process_modbus_response(response)

    def _process_modbus_response(self, deserialized_dict):
        self.user_action_state["current_response_received_time"] = datetime.now()
        if deserialized_dict != "-":
            for key in deserialized_dict:
                if key in self.user_action_state:
                    self.user_action_state[key] = deserialized_dict[key]
        self._update_history_last_ten()
        self._write_to_db()
        self.response_signal.emit(False)
        self.periodic_update_signal.emit(False)
        _set_currently_selected_automatic_request(self, "user")
        self.connection_info_signal.emit("User Response Received.")

    def _update_history_last_ten(self):
        if len(self.last_ten_dicts) >= 10:
            min_key = min(self.last_ten_dicts.keys())
            self.last_ten_dicts.pop(min_key)
        tid = deepcopy(self.user_action_state["current_tid"])
        self.last_ten_dicts[tid] = deepcopy(self.user_action_state)

    def _write_to_db(self):
        self.database.db_write(self.user_action_state)

    def _read_from_db(self):
        db_returned_values = self.database.db_read(self._historian_db_current_index)
        self._historian_db_dicts = db_returned_values
        self._historian_db_current_index = self._historian_db_current_index + 10

    def reset_db_dict(self):
        self._historian_db_dicts = {}
        self._historian_db_current_index = 0
