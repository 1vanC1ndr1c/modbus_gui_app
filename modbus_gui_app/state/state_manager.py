import asyncio
import functools
import queue
from concurrent.futures.thread import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime
from threading import Thread

from PySide2.QtCore import Signal, QObject

from modbus_gui_app.communication.modbus_connection import ModbusConnection
from modbus_gui_app.communication.user_request_serializer import read_coils_serialize, read_discrete_inputs_serialize, \
    read_holding_registers_serialize, read_input_registers_serialize, write_single_coil_serialize, \
    write_single_register_serialize
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.error_logging.error_logger import init_logger
from modbus_gui_app.state import state_manager_live_update
from modbus_gui_app.state.state_manager_data_structures import _init_user_action_state_dict, \
    _init_live_update_states
from modbus_gui_app.state.state_manager_live_update import _live_update_loop


class StateManager(QObject):
    """A class used to be the intermediate between the communication, database and the graphical interface of
      the application. All message routing and current values of the information (state) goes through an instance of
      this class.

      Attributes:
        response_signal(PySide2.QtCore.Signal):  Used to signal when there is a response ready to be shown
                                                within the GUI.
        periodic_update_signal(PySide2.QtCore.Signal): Used to signal when the periodic update is done refreshing
                                            the current information and that information is ready to be shown
                                            in the GUI.
        connection_info_signal(PySide2.QtCore.Signal): Used to signal that the connection has a new message
                                                        being sent or received.
        invalid_connection_signal: Used to signal that no connection was successfully established.

        last_ten_dicts(dict): A dictionary used to fetch and save the values from the database (ten at a time).

        database(database.db_handler.Backend): An instance of the Backend class that provides the connection to the
                                                database and the supporting functions for interacting with said
                                                database.

        gui_request_queue(queue.Queue): A queue through which the GUI sends the request data which is forwarded to the
                                        connection module.

        modbus_connection(communication.modbus_connection.ModbusConnection): An instance of the connection class
                                    that provides the methods needed to send and receive data.

        user_action_state(dict): A dictionary that stores the current request data and, when received, the corresponding
                                response data.

        gui(gui.window.Gui): An instance of the graphical user interface class.

        live_update_states(dict): A dictionary that contains the information about the last valid requests and
                                valid responses for every type of a request. Used to resend those requests periodically.

        ws_read_loop_future(asyncio.Future): The future of the web socket reader. Publicly exposed to that it can be
                            closed when the application is closing. By closing this read loop, other read loops also
                            stop.

        logger(logging.logger): An error logger used to record any errors that might occur during the program execution.
    """
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
        self.logger = init_logger(__name__)

    def get_historian_db_dicts(self):
        """A method that reads from the database and saves the results into a dictionary.

        Returns:
            dict: A dictionary containing the read data and data read before that.

        """
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
        # self.modbus_connection.live_update_states.update(self.live_update_states)
        await self.modbus_connection.open_session()
        self.connection_info_signal.emit("Connection Established")

        live_update_refresh_future = asyncio.ensure_future(_live_update_loop(self))
        state_manager_to_modbus_write_future = asyncio.ensure_future(self._gui_queue_read_loop())

        await asyncio.wait([live_update_refresh_future, state_manager_to_modbus_write_future],
                           return_when=asyncio.FIRST_COMPLETED)

        try:
            state_manager_to_modbus_write_future.cancel()
            live_update_refresh_future.cancel()
        except asyncio.CancelledError:
            pass

        try:
            await self.modbus_connection.ws.close()
        except Exception as conn_error:
            self.logger.exception("STATE MANAGER FUNCTIONS: Error When Connecting, No Connection.\n" + str(conn_error))
            self.invalid_connection_signal.emit("No Connection.")
            self.connection_info_signal.emit("No Connection.")

        await self.modbus_connection.session.close()

    async def _gui_queue_read_loop(self):
        executor = ThreadPoolExecutor(1)
        while True:
            gui_request_data = await asyncio.get_event_loop().run_in_executor(
                executor, functools.partial(self._get_msg_from_gui_queue))
            if gui_request_data[0] == "End.":
                self.modbus_connection.close_connection()
                break
            await self.send_request_to_modbus(gui_request_data)

    def _get_msg_from_gui_queue(self):
        request = self.gui_request_queue.get()
        return request

    async def send_request_to_modbus(self, gui_request_data):
        request_source = gui_request_data[1]
        gui_request_data = gui_request_data[0]
        function_code = gui_request_data[-1]
        tid = self.modbus_connection.tid + 1
        start_addr = gui_request_data[0]
        unit_addr = gui_request_data[2]
        response = None

        if function_code == 1:
            no_of_coils = gui_request_data[1]
            bytes_reg, results_dict = read_coils_serialize(start_addr, no_of_coils, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            else:
                self.live_update_states["current_read_coils"].update(results_dict)
            response = await self.modbus_connection.ws_read_coils(start_addr, no_of_coils, unit_addr)

        elif function_code == 2:
            input_count = gui_request_data[1]
            bytes_reg, results_dict = read_discrete_inputs_serialize(start_addr, input_count, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            else:
                self.live_update_states["current_read_discrete_inputs"].update(results_dict)
            response = await self.modbus_connection.ws_read_discrete_inputs(start_addr, input_count, unit_addr)

        elif function_code == 3:
            h_regs_count = gui_request_data[1]
            bytes_reg, results_dict = read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            else:
                self.live_update_states["current_read_holding_registers"].update(results_dict)
            response = await self.modbus_connection.ws_read_holding_registers(start_addr, h_regs_count, unit_addr)

        elif function_code == 4:
            in_regs_count = gui_request_data[1]
            bytes_reg, results_dict = read_input_registers_serialize(start_addr, in_regs_count, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            else:
                self.live_update_states["current_read_input_registers"].update(results_dict)
            response = await self.modbus_connection.ws_read_input_registers(start_addr, in_regs_count, unit_addr)

        elif function_code == 5:
            coil_state = gui_request_data[1]
            bytes_reg, results_dict = write_single_coil_serialize(start_addr, coil_state, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_write_single_coil(start_addr, coil_state, unit_addr)

        elif function_code == 6:
            reg_value = gui_request_data[1]
            bytes_reg, results_dict = write_single_register_serialize(start_addr, reg_value, unit_addr, tid)
            if request_source == "User Request.":
                self.user_action_state.update(results_dict)
                self.connection_info_signal.emit("User Request Sent.")
            response = await self.modbus_connection.ws_write_single_register(start_addr, reg_value, unit_addr)

        if response is not None:
            if request_source == "User Request.":
                self.user_action_state.update(self.modbus_connection.dicts_by_tid[tid])
                self._process_modbus_response(response)

            else:
                live_dict = {}
                if function_code == 1:
                    live_dict = self.live_update_states["current_read_coils"]
                elif function_code == 2:
                    live_dict = self.live_update_states["current_read_discrete_inputs"]
                elif function_code == 3:
                    live_dict = self.live_update_states["current_read_holding_registers"]
                elif function_code == 4:
                    live_dict = self.live_update_states["current_read_input_registers"]
                if len(live_dict) > 0:
                    live_dict.update(self.modbus_connection.dicts_by_tid[tid])
                    state_manager_live_update.process_live_update_response(response, live_dict)

    def _process_modbus_response(self, new_dict):
        self.user_action_state["current_response_received_time"] = datetime.now()
        if new_dict != "-":
            for key in new_dict:
                if key in self.user_action_state:
                    self.user_action_state[key] = new_dict[key]
        self._update_history_last_ten()
        self._write_to_db()
        self.response_signal.emit(False)
        self.periodic_update_signal.emit(False)
        state_manager_live_update.set_currently_selected_automatic_request(self, "user")
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
        """A method used to reset the data that was read from the database and is currently stored in a dictionary.

        """
        self._historian_db_dicts = {}
        self._historian_db_current_index = 0
