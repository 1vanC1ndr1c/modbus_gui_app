import logging
import re
from datetime import datetime

from modbus_gui_app.communication import response_deserializer
from modbus_gui_app.state.data_structures import _init_live_update_states

live_update_states_test_dict = _init_live_update_states()


def test_read_coils_deserialize():
    read_coils_dict = live_update_states_test_dict["current_read_coils"]
    modbus_response = read_coils_dict["current_response_serialized"]
    modbus_response = re.findall('..', str(modbus_response.hex()))
    modbus_response = modbus_response[9:]
    start_addr = str(1)
    response_dict = {}

    response_deserializer.read_coils_deserialize(modbus_response, start_addr, response_dict)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == read_coils_dict[key]


def test_read_discrete_inputs_deserialize():
    read_disc_ins_dict = live_update_states_test_dict["current_read_discrete_inputs"]
    modbus_response = read_disc_ins_dict["current_response_serialized"]
    modbus_response = re.findall('..', str(modbus_response.hex()))
    modbus_response = modbus_response[9:]
    start_addr = str(1)
    response_dict = {}

    response_deserializer.read_discrete_inputs_deserialize(modbus_response, start_addr, response_dict)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == read_disc_ins_dict[key]


def test_read_holding_registers_deserialize():
    read_h_regs_dict = live_update_states_test_dict["current_read_holding_registers"]
    modbus_response = read_h_regs_dict["current_response_serialized"]
    modbus_response = re.findall('..', str(modbus_response.hex()))
    modbus_response = modbus_response[9:]
    start_addr = str(1)
    response_dict = {}

    logger = logging.getLogger()
    response_deserializer.read_holding_registers_deserialize(modbus_response, start_addr, response_dict, logger)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == read_h_regs_dict[key]


def test_read_input_registers_deserialize():
    read_in_regs_dict = live_update_states_test_dict["current_read_input_registers"]
    modbus_response = read_in_regs_dict["current_response_serialized"]
    modbus_response = re.findall('..', str(modbus_response.hex()))
    modbus_response = modbus_response[9:]
    start_addr = str(1)
    response_dict = {}

    logger = logging.getLogger()
    response_deserializer.read_holding_registers_deserialize(modbus_response, start_addr, response_dict, logger)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == read_in_regs_dict[key]


def test_write_single_coil_deserialize():
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
    modbus_response = write_coils_dict["current_response_serialized"]
    response_dict = {}

    response_deserializer.write_single_coil_deserialize(response_dict, modbus_response)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == write_coils_dict[key]


def test_write_single_register_deserialize():
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
    modbus_response = write_regs_dict["current_response_serialized"]
    response_dict = {}

    response_deserializer.write_single_register_deserialize(response_dict, modbus_response)

    assert len(response_dict) != 0

    for key in response_dict:
        assert response_dict[key] is not None

    for key in response_dict:
        assert response_dict[key] == write_regs_dict[key]
