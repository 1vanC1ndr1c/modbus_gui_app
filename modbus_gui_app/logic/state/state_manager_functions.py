import asyncio
import functools
from concurrent.futures.thread import ThreadPoolExecutor
from copy import deepcopy
from threading import Thread

from modbus_gui_app.communication.modbus_connection import ModbusConnection
from modbus_gui_app.logic.state.state_manager_data_structures import *
from modbus_gui_app.logic.state.state_manager_live_update import set_currently_selected_automatic_request

from modbus_gui_app.gui.error_window import init_error_window


def init_state():
    current_request_and_response_dictionary = init_current_request_and_response_dictionary()
    return current_request_and_response_dictionary


# connect to modbus
def start_communications_thread(state_manager):
    communications_thread = Thread(
        target=lambda: asyncio.new_event_loop().run_until_complete(start_readers_and_writers(state_manager)))
    communications_thread.start()


async def start_readers_and_writers(state_manager):
    state_manager.modbus_connection = ModbusConnection()
    state_manager.modbus_connection.set_state_manager(state_manager)
    await state_manager.modbus_connection.connect_with_modbus()
    state_manager.connection_info_signal.emit("Connection Established")

    current_state_periodic_refresh_future = asyncio.ensure_future(state_manager.current_state_periodic_refresh())
    state_manager.current_state_periodic_refresh_future = current_state_periodic_refresh_future
    ws_read_loop_future = asyncio.ensure_future(state_manager.modbus_connection.ws_read_loop())
    state_manager_to_modbus_write_future = asyncio.ensure_future(gui_to_state_manager_write(state_manager))

    await asyncio.wait(
        [ws_read_loop_future, current_state_periodic_refresh_future, state_manager_to_modbus_write_future],
        return_when=asyncio.FIRST_COMPLETED)

    ws_read_loop_future.cancel()
    state_manager_to_modbus_write_future.cancel()
    current_state_periodic_refresh_future.cancel()
    try:
        await state_manager.modbus_connection.ws.close()
    except Exception as conn_error:
        print("STATE MANAGER FUNCTIONS: Error When Connecting, No Connection. ", conn_error)
        state_manager.invalid_connection_signal.emit("No Connection.")
        state_manager.connection_info_signal.emit("No Connection.")

    await state_manager.modbus_connection.session.close()


# user communication
async def gui_to_state_manager_write(state_manager):
    executor = ThreadPoolExecutor(1)
    while True:
        valid_gui_request = await asyncio.get_event_loop().run_in_executor(executor, functools.partial(
            get_msg_from_gui_queue, state_manager))
        await send_request_to_modbus(state_manager, valid_gui_request)


def get_msg_from_gui_queue(state_manager):
    request = state_manager.gui_request_queue.get()
    return request


async def send_request_to_modbus(state_manager, valid_gui_request):
    # send the validated data(in a dict) to COMM
    state_manager.current_request_and_response_dictionary["current_request_from_gui"] = valid_gui_request
    state_manager.current_request_and_response_dictionary["current_request_from_gui_is_valid"] = True
    state_manager.current_request_and_response_dictionary["current_request_from_gui_error_msg"] = "-"
    state_manager.current_request_and_response_dictionary["current_request_sent_time"] = datetime.now()
    state_manager.connection_info_signal.emit("User Request Sent.")
    response = await state_manager.modbus_connection.ws_write(state_manager.current_request_and_response_dictionary)
    process_modbus_response(state_manager, response)


def process_modbus_response(state_manager, deserialized_dict):
    state_manager.current_request_and_response_dictionary["current_response_received_time"] = datetime.now()
    if deserialized_dict != "-":
        for key in deserialized_dict:
            if key in state_manager.current_request_and_response_dictionary:
                state_manager.current_request_and_response_dictionary[key] = deserialized_dict[key]
    # dictionary housekeeping
    state_manager.update_history_last_ten()
    state_manager.state_manager_write_to_db()
    state_manager.response_signal.emit(False)  # signal the gui and process the change
    state_manager.periodic_update_signal.emit(False)
    set_currently_selected_automatic_request(state_manager, "user")
    state_manager.connection_info_signal.emit("User Response Received.")


# internal data and database
def update_history_last_ten(state_manager):
    if len(state_manager.last_ten_dicts) >= 10:  # save only the last 10. If more, delete the oldest one.
        min_key = min(state_manager.last_ten_dicts.keys())
        state_manager.last_ten_dicts.pop(min_key)
    # use deepcopy, otherwise, the older data will be overwritten
    tid = deepcopy(state_manager.current_request_and_response_dictionary["current_tid"])
    state_manager.last_ten_dicts[tid] = deepcopy(state_manager.current_request_and_response_dictionary)


def state_manager_write_to_db(state_manager):
    state_manager.database.db_write(state_manager.current_request_and_response_dictionary)


def state_manager_read_from_db(state_manager):
    state_manager.database.db_read(state_manager.historian_db_current_index)
    state_manager.historian_db_current_index = state_manager.historian_db_current_index + 10


def reset_db_dict(state_manager):
    state_manager.historian_db_dicts = {}
    state_manager.historian_db_current_index = 0
