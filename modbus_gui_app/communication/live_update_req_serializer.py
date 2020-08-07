import re
from datetime import datetime


def _automatic_request_serialize(live_update_states):
    function_code = live_update_states["currently_selected_function"]

    if function_code == "01":
        _read_coils_automatic_request_serialize(live_update_states)
    elif function_code == "02":
        _read_discrete_inputs_automatic_request_serialize(live_update_states)
    elif function_code == "03":
        _read_holding_registers_automatic_request_serialize(live_update_states)
    elif function_code == "04":
        _read_input_registers_automatic_request_serialize(live_update_states)


def _read_coils_automatic_request_serialize(live_update_states):
    old_request = live_update_states["current_request"]
    current_tid = live_update_states["read_coils_tid"]
    valid = live_update_states["current_read_coils"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_request_serialized"] = new_request
    live_update_states["current_read_coils"]["current_request_serialized"] = new_request
    live_update_states["current_read_coils"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request
    live_update_states["current_tid"] = current_tid


def _read_discrete_inputs_automatic_request_serialize(live_update_states):
    old_request = live_update_states["current_request"]
    current_tid = live_update_states["read_discrete_inputs_tid"]
    valid = live_update_states["current_read_discrete_inputs"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x02\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_request_serialized"] = new_request
    live_update_states["current_read_discrete_inputs"]["current_request_serialized"] = new_request
    live_update_states["current_read_discrete_inputs"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request
    live_update_states["current_tid"] = current_tid


def _read_holding_registers_automatic_request_serialize(live_update_states):
    old_request = live_update_states["current_request"]
    current_tid = live_update_states["read_holding_registers_tid"]
    valid = live_update_states["current_read_holding_registers"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_request_serialized"] = new_request
    live_update_states["current_read_holding_registers"]["current_request_serialized"] = new_request
    live_update_states["current_read_holding_registers"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request
    live_update_states["current_tid"] = current_tid


def _read_input_registers_automatic_request_serialize(live_update_states):
    old_request = live_update_states["current_request"]
    current_tid = live_update_states["read_input_registers_tid"]

    valid = live_update_states["current_read_input_registers"]["current_request_from_gui_is_valid"]
    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x04\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_request_serialized"] = new_request
    live_update_states["current_read_input_registers"]["current_request_serialized"] = new_request
    live_update_states["current_read_input_registers"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request
    live_update_states["current_tid"] = current_tid
