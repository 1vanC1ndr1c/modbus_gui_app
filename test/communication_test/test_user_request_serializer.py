from copy import deepcopy
from datetime import datetime

from modbus_gui_app.communication import request_serializer
from modbus_gui_app.state.state_manager_data_structures import _init_live_update_states

live_update_states_test_dict = _init_live_update_states()


def test_read_coils_serialize():
    read_coils_dict = _init_live_update_states()
    read_coils_dict = deepcopy(read_coils_dict["current_read_coils"])
    read_coils_dict["current_tid"] = 1
    read_coils_dict["current_unit_address"] = str(1)
    old_bytes = read_coils_dict["current_request_serialized"]
    data = read_coils_dict["current_request_from_gui"]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.read_coils_serialize(start_addr, no_of_coils, unit_addr, tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == read_coils_dict[key]


def test_read_discrete_inputs_serialize():
    read_coils_dict = _init_live_update_states()
    read_coils_dict = deepcopy(read_coils_dict["current_read_discrete_inputs"])
    read_coils_dict["current_tid"] = 1
    read_coils_dict["current_unit_address"] = str(1)
    old_bytes = read_coils_dict["current_request_serialized"]
    data = read_coils_dict["current_request_from_gui"]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.read_discrete_inputs_serialize(start_addr, no_of_coils, unit_addr,
                                                                            tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == read_coils_dict[key]


def test_read_holding_registers_serialize():
    read_coils_dict = _init_live_update_states()
    read_coils_dict = deepcopy(read_coils_dict["current_read_holding_registers"])
    read_coils_dict["current_tid"] = 1
    read_coils_dict["current_unit_address"] = str(1)
    old_bytes = read_coils_dict["current_request_serialized"]
    data = read_coils_dict["current_request_from_gui"]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.read_holding_registers_serialize(start_addr, no_of_coils, unit_addr,
                                                                              tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == read_coils_dict[key]


def test_read_input_registers_serialize():
    read_coils_dict = _init_live_update_states()
    read_coils_dict = deepcopy(read_coils_dict["current_read_input_registers"])
    read_coils_dict["current_tid"] = 1
    read_coils_dict["current_unit_address"] = str(1)
    old_bytes = read_coils_dict["current_request_serialized"]
    data = read_coils_dict["current_request_from_gui"]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.read_input_registers_serialize(start_addr, no_of_coils, unit_addr,
                                                                            tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == read_coils_dict[key]


def test_write_single_coil_serialize():
    write_coils_dict = {
        'current_tid': 1,
        'current_unit_address': '1',
        'current_function_code': '05',
        'current_request_name': 'Write Single Coil.',
        'current_request_from_gui': [1, 1, 1, 5],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00',
        'current_response_is_valid': True,
        'current_response_err_msg': '-',
        'current_response_returned_values': ['00', '01', '00', '00', '00', '06', '01', '05', '00', '00', 'ff', '00']
    }

    old_bytes = write_coils_dict["current_response_serialized"]

    data = [1, 1, 1, 5]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.write_single_coil_serialize(start_addr, no_of_coils, unit_addr,
                                                                         tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == write_coils_dict[key]


def test_write_single_register_serialize():
    write_regs_dict = {
        'current_tid': 1,
        'current_unit_address': '1',
        'current_function_code': '06',
        'current_request_name': 'Write Single Register.',
        'current_request_from_gui': [1, 1, 1, 6],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x06\x00\x00\x00\x01',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x06\x00\x00\x00\x01',
        'current_response_is_valid': True, 'current_response_err_msg': '-',
        'current_response_returned_values': ['00', '01', '00', '00', '00', '06', '01', '06', '00', '00', '00', '01']
    }
    old_bytes = write_regs_dict["current_response_serialized"]

    data = [1, 1, 1, 5]
    start_addr = data[0]
    no_of_coils = data[1]
    unit_addr = data[2]
    tid = 1
    new_bytes, new_dict = request_serializer.write_single_register_serialize(start_addr, no_of_coils, unit_addr,
                                                                             tid)

    assert new_bytes == old_bytes

    for key in new_dict:
        assert new_dict[key] == write_regs_dict[key]
