import re

from modbus_gui_app.communication import live_update_req_serializer
from modbus_gui_app.state.data_structures import _init_live_update_states

live_update_states_test_dict = _init_live_update_states()


def test_read_coils_automatic_request_serialize():
    for tid in range(1, 0xffff):
        live_update_states_test_dict["current_tid"] = int(str(hex(tid))[2:].rjust(4, '0'), 16)
        str_tid = str(hex(live_update_states_test_dict["current_tid"]))[2:].rjust(4, '0')
        old_request = live_update_states_test_dict["current_read_coils"]["current_request_serialized"]
        live_update_states_test_dict["current_request"] = old_request
        old_request = bytes.fromhex(str(str_tid) + ''.join(re.findall('..', str(old_request.hex()))[2:]))
        live_update_req_serializer._read_coils_automatic_request_serialize(live_update_states_test_dict)
        new_request = live_update_states_test_dict["current_request"]

        if old_request != b'0':
            assert old_request == new_request


def test_read_discrete_inputs_automatic_request_serialize():
    for tid in range(1, 0xffff):
        live_update_states_test_dict["current_tid"] = int(str(hex(tid))[2:].rjust(4, '0'), 16)
        str_tid = str(hex(live_update_states_test_dict["current_tid"]))[2:].rjust(4, '0')
        old_request = live_update_states_test_dict["current_read_discrete_inputs"]["current_request_serialized"]
        live_update_states_test_dict["current_request"] = old_request
        old_request = bytes.fromhex(str(str_tid) + ''.join(re.findall('..', str(old_request.hex()))[2:]))
        live_update_req_serializer._read_discrete_inputs_automatic_request_serialize(live_update_states_test_dict)
        new_request = live_update_states_test_dict["current_request"]
        if old_request != b'0':
            assert old_request == new_request


def test_read_holding_registers_automatic_request_serialize():
    for tid in range(1, 0xffff):
        live_update_states_test_dict["current_tid"] = int(str(hex(tid))[2:].rjust(4, '0'), 16)
        str_tid = str(hex(live_update_states_test_dict["current_tid"]))[2:].rjust(4, '0')
        old_request = live_update_states_test_dict["current_read_holding_registers"]["current_request_serialized"]
        live_update_states_test_dict["current_request"] = old_request
        old_request = bytes.fromhex(str(str_tid) + ''.join(re.findall('..', str(old_request.hex()))[2:]))
        live_update_req_serializer._read_discrete_inputs_automatic_request_serialize(live_update_states_test_dict)
        new_request = live_update_states_test_dict["current_request"]
        if old_request != b'0':
            assert old_request == new_request


def test_read_input_registers_automatic_request_serialize():
    for tid in range(1, 0xffff):
        live_update_states_test_dict["current_tid"] = int(str(hex(tid))[2:].rjust(4, '0'), 16)
        str_tid = str(hex(live_update_states_test_dict["current_tid"]))[2:].rjust(4, '0')
        old_request = live_update_states_test_dict["current_read_input_registers"]["current_request_serialized"]
        live_update_states_test_dict["current_request"] = old_request
        old_request = bytes.fromhex(str(str_tid) + ''.join(re.findall('..', str(old_request.hex()))[2:]))
        live_update_req_serializer._read_discrete_inputs_automatic_request_serialize(live_update_states_test_dict)
        new_request = live_update_states_test_dict["current_request"]
        if old_request != b'0':
            assert old_request == new_request
