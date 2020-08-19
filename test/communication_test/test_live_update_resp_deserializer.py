import re
from copy import deepcopy

from modbus_gui_app.error_logging.error_logger import init_logger

from modbus_gui_app.communication import live_update_resp_deserializer
from modbus_gui_app.state.data_structures import _init_live_update_states

live_update_states_test_dict = _init_live_update_states()


def test_read_coils_live_update_deserialize():
    bytes_response = live_update_states_test_dict["current_read_coils"]["current_response_serialized"]
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    old_dict = deepcopy(live_update_states_test_dict["current_read_coils"])

    live_update_resp_deserializer._read_coils_live_update_deserialize(live_update_states_test_dict, hex_response_array,
                                                                      deser_dict)

    new_dict = deepcopy(live_update_states_test_dict["current_read_coils"])

    for key in old_dict:
        if key != "current_request_sent_time" and key != "current_response_received_time":
            assert old_dict[key] == new_dict[key]

    resp = b'\x00\x02\x00\x00\x00\x06\x01\x01\x04\x03\x02\x01'
    resp = re.findall('..', str(resp.hex()))
    old_dict = deepcopy(live_update_states_test_dict["current_read_coils"])
    live_update_resp_deserializer._read_coils_live_update_deserialize(live_update_states_test_dict, resp,
                                                                      deser_dict)
    new_dict = deepcopy(live_update_states_test_dict["current_read_coils"])
    for key in old_dict:
        if key == "current_response_returned_values":
            assert old_dict[key] != new_dict[key]


def test_read_discrete_inputs_live_update_deserialize():
    bytes_response = live_update_states_test_dict["current_read_discrete_inputs"]["current_response_serialized"]
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    old_dict = deepcopy(live_update_states_test_dict["current_read_discrete_inputs"])

    live_update_resp_deserializer._read_discrete_inputs_live_update_deserialize(live_update_states_test_dict,
                                                                                hex_response_array,
                                                                                deser_dict)

    new_dict = deepcopy(live_update_states_test_dict["current_read_discrete_inputs"])

    for key in old_dict:
        if key != "current_request_sent_time" and key != "current_response_received_time":
            assert old_dict[key] == new_dict[key]

    resp = b'\x00\x02\x00\x00\x00\x06\x02\x01\x04\x03\x02\x01'
    resp = re.findall('..', str(resp.hex()))
    old_dict = deepcopy(live_update_states_test_dict["current_read_discrete_inputs"])
    live_update_resp_deserializer._read_discrete_inputs_live_update_deserialize(live_update_states_test_dict, resp,
                                                                                deser_dict)
    new_dict = deepcopy(live_update_states_test_dict["current_read_discrete_inputs"])
    for key in old_dict:
        if key == "current_response_returned_values":
            assert old_dict[key] != new_dict[key]


def test_read_holding_registers_live_update_deserialize():
    bytes_response = live_update_states_test_dict["current_read_holding_registers"]["current_response_serialized"]
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    old_dict = deepcopy(live_update_states_test_dict["current_read_holding_registers"])

    live_update_resp_deserializer._read_holding_registers_live_update_deserialize(live_update_states_test_dict,
                                                                                  hex_response_array,
                                                                                  deser_dict, None)

    new_dict = deepcopy(live_update_states_test_dict["current_read_holding_registers"])

    for key in old_dict:
        if key != "current_request_sent_time" and key != "current_response_received_time":
            assert old_dict[key] == new_dict[key]

    resp = b'\x00\x02\x00\x00\x00\x06\x02\x01\x04\x03\x02\x01'
    resp = re.findall('..', str(resp.hex()))
    old_dict = deepcopy(live_update_states_test_dict["current_read_holding_registers"])
    live_update_resp_deserializer._read_holding_registers_live_update_deserialize(live_update_states_test_dict, resp,
                                                                                  deser_dict, init_logger(__name__))
    new_dict = deepcopy(live_update_states_test_dict["current_read_holding_registers"])
    for key in old_dict:
        if key == "current_response_returned_values":
            assert old_dict[key] != new_dict[key]


def test_read_input_registers_live_update_deserialize():
    bytes_response = live_update_states_test_dict["current_read_input_registers"]["current_response_serialized"]
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    old_dict = deepcopy(live_update_states_test_dict["current_read_input_registers"])

    live_update_resp_deserializer._read_input_registers_live_update_deserialize(live_update_states_test_dict,
                                                                                hex_response_array,
                                                                                deser_dict, None)

    new_dict = deepcopy(live_update_states_test_dict["current_read_input_registers"])

    for key in old_dict:
        if key != "current_request_sent_time" and key != "current_response_received_time":
            assert old_dict[key] == new_dict[key]

    resp = b'\x00\x02\x00\x00\x00\x06\x02\x01\x04\x03\x02\x01'
    resp = re.findall('..', str(resp.hex()))
    old_dict = deepcopy(live_update_states_test_dict["current_read_input_registers"])
    live_update_resp_deserializer._read_input_registers_live_update_deserialize(live_update_states_test_dict, resp,
                                                                                deser_dict, init_logger(__name__))
    new_dict = deepcopy(live_update_states_test_dict["current_read_input_registers"])
    for key in old_dict:
        if key == "current_response_returned_values":
            assert old_dict[key] != new_dict[key]
