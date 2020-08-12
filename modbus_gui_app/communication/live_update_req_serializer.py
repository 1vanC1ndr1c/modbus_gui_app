import re
from datetime import datetime


def _automatic_request_serialize(live_update_states, tid):
    """ This function picks the correct serialization function based on the function code found in live_update_states.

    Args:
        live_update_states(dict): The dictionary that needs to be updated with the current automated request data.
        tid(int): The transaction id that will be used in the request.

    Returns:
        bytes, dict: Bytes of the request that is serialized, and the dictionary that contains the information
                    about the serialization.
    """
    function_code = live_update_states["currently_selected_function"]
    live_update_states["current_tid"] = int(str(hex(tid))[2:].rjust(4, '0'), 16)

    live_update_states["current_tid"] = tid
    if function_code == "01":
        _read_coils_automatic_request_serialize(live_update_states)
    elif function_code == "02":
        _read_discrete_inputs_automatic_request_serialize(live_update_states)
    elif function_code == "03":
        _read_holding_registers_automatic_request_serialize(live_update_states)
    elif function_code == "04":
        _read_input_registers_automatic_request_serialize(live_update_states)


def _read_coils_automatic_request_serialize(live_update_states):
    """This function updates the dictionary by giving the previous valid request a new transaction ID.
        It then updates the dictionary with new values.

    Args:
        live_update_states(dict): The dictionary that contains the previous request. The updated request is saved into it.
    """
    old_request = live_update_states["current_request"]
    current_tid = str(hex(live_update_states["current_tid"]))[2:].rjust(4, '0')
    valid = live_update_states["current_read_coils"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_read_coils"]["current_request_serialized"] = new_request
    live_update_states["current_read_coils"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request


def _read_discrete_inputs_automatic_request_serialize(live_update_states):
    """This function updates the dictionary by giving the previous valid request a new transaction ID.
        It then updates the dictionary with new values.

    Args:
        live_update_states(dict): The dictionary that contains the previous request. The updated request is saved into it.
    """
    old_request = live_update_states["current_request"]
    current_tid = str(hex(live_update_states["current_tid"]))[2:].rjust(4, '0')
    valid = live_update_states["current_read_discrete_inputs"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x02\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_read_discrete_inputs"]["current_request_serialized"] = new_request
    live_update_states["current_read_discrete_inputs"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request


def _read_holding_registers_automatic_request_serialize(live_update_states):
    """This function updates the dictionary by giving the previous valid request a new transaction ID.
        It then updates the dictionary with new values.

    Args:
        live_update_states(dict): The dictionary that contains the previous request.
        The updated request is saved into it.
    """
    old_request = live_update_states["current_request"]
    current_tid = str(hex(live_update_states["current_tid"]))[2:].rjust(4, '0')
    valid = live_update_states["current_read_holding_registers"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_read_holding_registers"]["current_request_serialized"] = new_request
    live_update_states["current_read_holding_registers"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request


def _read_input_registers_automatic_request_serialize(live_update_states):
    """This function updates the dictionary by giving the previous valid request a new transaction ID.
        It then updates the dictionary with new values.

    Args:
        live_update_states(dict): The dictionary that contains the previous request.
        The updated request is saved into it.
    """
    old_request = live_update_states["current_request"]
    current_tid = str(hex(live_update_states["current_tid"]))[2:].rjust(4, '0')
    valid = live_update_states["current_read_input_registers"]["current_request_from_gui_is_valid"]

    if old_request == b'0' or valid is False:
        old_request = b'\x00\x01\x00\x00\x00\x06\x01\x04\x00\x00\x00\x14'
    old_request = re.findall('..', str(old_request.hex()))[2:]
    new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))

    live_update_states["current_read_input_registers"]["current_request_serialized"] = new_request
    live_update_states["current_read_input_registers"]["current_request_sent_time"] = datetime.now()
    live_update_states["current_request"] = new_request
