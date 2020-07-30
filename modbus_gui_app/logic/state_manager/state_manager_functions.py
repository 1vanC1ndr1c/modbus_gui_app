import asyncio
import functools
from concurrent.futures.thread import ThreadPoolExecutor
from copy import deepcopy
from threading import Thread
from datetime import datetime

from modbus_gui_app.communication.modbus_connection import ModbusConnection


def init_state():
    current_request_and_response_dictionary = {
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

    current_state_periodic_refresh_future = asyncio.ensure_future(state_manager.current_state_periodic_refresh())
    ws_read_loop_future = asyncio.ensure_future(state_manager.modbus_connection.ws_read_loop())
    state_manager_to_modbus_write_future = asyncio.ensure_future(gui_to_state_manager_write(state_manager))

    await asyncio.wait(
        [ws_read_loop_future, current_state_periodic_refresh_future, state_manager_to_modbus_write_future],
        return_when=asyncio.FIRST_COMPLETED)

    ws_read_loop_future.cancel()
    state_manager_to_modbus_write_future.cancel()
    current_state_periodic_refresh_future.cancel()

    await state_manager.modbus_connection.ws.close()
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


# functions that deal with updating the current status in the lower part of the GUI.
async def current_state_periodic_refresh(state_manager):
    while True:
        set_currently_selected_automatic_request(state_manager, "automatic")
        await state_manager.modbus_connection.ws_refresh()

        if state_manager.current_coil_input_reg_states["currently_selected_function"] == "01":
            state_manager.periodic_update_signal.emit(False)
        else:
            pass
        await asyncio.sleep(5)


def init_current_states():
    current_read_coils = {
        'current_tid': 1,
        'current_unit_address': '01',
        'current_function_code': '01',
        'current_request_name': 'Read Coils.',
        'current_request_from_gui': [1, 20, 1, 1],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x01\x03\x00\x00\x00',
        'current_response_is_valid': True, 'current_response_err_msg': '-',
        'current_response_returned_values': '-'
    }

    current_coil_input_reg_states = {
        "current_request": b'0',
        "current_tid": 9901,
        "currently_selected_function": "01",
        "current_read_coils": current_read_coils,
        "read_coils_tid": 9901
    }
    return current_coil_input_reg_states


def set_currently_selected_automatic_request(state_manager, source):
    current_function_code = state_manager.gui.left_side_select_operation_box.currentIndex() + 1

    if current_function_code == 1 or current_function_code == 2 \
            or current_function_code == 3 or current_function_code == 4:

        current_function_code = str(hex(current_function_code))[2:].rjust(2, '0')
        state_manager.current_coil_input_reg_states["currently_selected_function"] = current_function_code

        if current_function_code == "01":
            update_current_coils_state(state_manager, source)



def update_current_coils_state(state_manager, source):
    if source == "user":
        current_state = state_manager.current_request_and_response_dictionary
        state_manager.current_coil_input_reg_states["current_read_coils"] = current_state
    elif source == "automatic":
        current_tid = state_manager.current_coil_input_reg_states["read_coils_tid"]
        new_dict = state_manager.current_coil_input_reg_states["current_read_coils"]
        new_dict["current_tid"] = current_tid
        state_manager.current_coil_input_reg_states["current_read_coils"] = new_dict