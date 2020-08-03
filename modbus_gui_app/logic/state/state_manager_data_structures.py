from datetime import datetime


def init_current_request_and_response_dictionary():
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


def init_current_coil_input_reg_states():
    time_stamp = datetime.now()

    current_read_coils = {
        'current_tid': 9901,
        'current_unit_address': '01',
        'current_function_code': '01',
        'current_request_name': 'Read Coils.',
        'current_request_from_gui': [1, 20, 1, 1],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14',
        'current_request_sent_time': time_stamp,
        'current_response_received_time': time_stamp,
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x01\x03\x00\x00\x00',
        'current_response_is_valid': True,
        'current_response_err_msg': '-',
        'current_response_returned_values': '-'
    }
    current_read_discrete_inputs = {
        'current_tid': 9902,
        'current_unit_address': '01',
        'current_function_code': '02',
        'current_request_name': 'Read Discrete Inputs .',
        'current_request_from_gui': [1, 20, 1, 2],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x02\x00\x00\x00\x14',
        'current_request_sent_time': time_stamp,
        'current_response_received_time': time_stamp,
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x02\x03\x00\x00\x00',
        'current_response_is_valid': True,
        'current_response_err_msg': '-',
        'current_response_returned_values': '-'
    }

    current_read_holding_registers = {
        'current_tid': 1,
        'current_unit_address': '01',
        'current_function_code': '03',
        'current_request_name': 'Read Holding Registers.',
        'current_request_from_gui': [1, 20, 1, 3],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x14',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00+\x01\x03('
                                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x00',
        'current_response_is_valid': True,
        'current_response_err_msg': '-',
        'current_response_returned_values': '-'
    }

    current_coil_input_reg_states = {
        "current_request": b'0',
        "current_tid": 9901,
        "currently_selected_function": "01",
        "current_read_coils": current_read_coils,
        "current_read_discrete_inputs": current_read_discrete_inputs,
        "current_read_holding_registers": current_read_holding_registers,
        "read_coils_tid": 9901,
        "read_discrete_inputs_tid": 9902,
        "read_holding_registers_tid": 9903
    }
    return current_coil_input_reg_states
