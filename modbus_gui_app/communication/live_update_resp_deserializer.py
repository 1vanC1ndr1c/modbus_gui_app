import re
from datetime import datetime

from modbus_gui_app.communication.user_response_deserializer import _read_coils_deserialize, \
    _check_for_response_errors, _read_discrete_inputs_deserialize, \
    _read_holding_registers_deserialize, _read_input_registers_deserialize
from modbus_gui_app.error_logging.error_logger import init_logger


def _live_update_response_deserialize(live_update_states, bytes_response):
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    logger = init_logger(__name__)
    is_without_errors = _check_for_response_errors(deser_dict, hex_response_array, logger)

    if is_without_errors is True:
        function_code = int(live_update_states["currently_selected_function"])
        if function_code == 1:
            _read_coils_live_update_deserialize(live_update_states, hex_response_array, deser_dict)
        elif function_code == 2:
            _read_discrete_inputs_live_update_deserialize(live_update_states, hex_response_array, deser_dict)
        elif function_code == 3:
            _read_holding_registers_live_update_deserialize(live_update_states, hex_response_array, deser_dict, logger)
        elif function_code == 4:
            _read_input_registers_live_update_deserialize(live_update_states, hex_response_array, deser_dict, logger)


def _read_coils_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict):
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_coils"]["current_request_from_gui"][0])

    deserialize_dict = _read_coils_deserialize(modbus_response, start_add, deserialize_dict)
    deserialize_dict["current_response_received_time"] = datetime.now()

    for key in deserialize_dict:
        if key in live_update_states["current_read_coils"]:
            live_update_states["current_read_coils"][key] = deserialize_dict[key]


def _read_discrete_inputs_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict):
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_discrete_inputs"]["current_request_from_gui"][0])

    deserialize_dict = _read_discrete_inputs_deserialize(modbus_response, start_add, deserialize_dict)

    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_discrete_inputs"]:
            live_update_states["current_read_discrete_inputs"][key] = deserialize_dict[key]


def _read_holding_registers_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict, logger):
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_holding_registers"]["current_request_from_gui"][0])

    deserialize_dict = _read_holding_registers_deserialize(modbus_response, start_add, deserialize_dict, logger)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_holding_registers"]:
            live_update_states["current_read_holding_registers"][key] = deserialize_dict[key]


def _read_input_registers_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict, logger):
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_input_registers"]["current_request_from_gui"][0])

    deserialize_dict = _read_input_registers_deserialize(modbus_response, start_add, deserialize_dict, logger)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_input_registers"]:
            live_update_states["current_read_input_registers"][key] = deserialize_dict[key]
