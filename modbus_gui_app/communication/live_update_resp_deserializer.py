import re
from datetime import datetime

from modbus_gui_app.communication.user_response_deserializer import read_coils_deserialize, \
    check_for_response_errors, read_discrete_inputs_deserialize, \
    read_holding_registers_deserialize, read_input_registers_deserialize
from modbus_gui_app.error_logging.error_logger import init_logger


def _live_update_response_deserialize(live_update_states, bytes_response):
    """This function is used to pick the right deserialization function based on the function code.
    Args:
        live_update_states: The dictionary that contains the request and is updated with the deserialized values.
        bytes_response: The response that needs to be deserialized.
    """
    deser_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    logger = init_logger(__name__)
    is_without_errors = check_for_response_errors(deser_dict, hex_response_array, logger)

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
    """This function deserializes the input response based on the information found in the live_update_states
        dictionary, calls the function that does the deserialization (deserialize()), which saves the result into
        a dictionary.
    Args:
        live_update_states(dict): State dictionary that contains the corresponding request and will contain deserialized
                            response.
        hex_response_array(list): Response bytes that are split into an array
        deserialize_dict(dict): A dictionary that contains the information about the request and response (both
                                serialized and unserialized).
    Returns:
    """
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_coils"]["current_request_from_gui"][0])

    deserialize_dict = read_coils_deserialize(modbus_response, start_add, deserialize_dict)
    deserialize_dict["current_response_received_time"] = datetime.now()

    for key in deserialize_dict:
        if key in live_update_states["current_read_coils"]:
            live_update_states["current_read_coils"][key] = deserialize_dict[key]


def _read_discrete_inputs_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict):
    """This function deserializes the input response based on the information found in the live_update_states
        dictionary, calls the function that does the deserialization (deserialize()), which saves the result into
        a dictionary.
    Args:
        live_update_states(dict): State dictionary that contains the corresponding request and will contain deserialized
                            response.
        hex_response_array(list): Response bytes that are split into an array
        deserialize_dict(dict): A dictionary that contains the information about the request and response (both
                                serialized and unserialized).
    Returns:
    """
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_discrete_inputs"]["current_request_from_gui"][0])

    deserialize_dict = read_discrete_inputs_deserialize(modbus_response, start_add, deserialize_dict)

    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_discrete_inputs"]:
            live_update_states["current_read_discrete_inputs"][key] = deserialize_dict[key]


def _read_holding_registers_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict, logger):
    """This function deserializes the input response based on the information found in the live_update_states
        dictionary, calls the function that does the deserialization (deserialize()), which saves the result into
        a dictionary.
    Args:
        live_update_states(dict): State dictionary that contains the corresponding request and will contain deserialized
                            response.
        hex_response_array(list): Response bytes that are split into an array
        deserialize_dict(dict): A dictionary that contains the information about the request and response (both
                                serialized and unserialized).
    Returns:
    """
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_holding_registers"]["current_request_from_gui"][0])

    deserialize_dict = read_holding_registers_deserialize(modbus_response, start_add, deserialize_dict, logger)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_holding_registers"]:
            live_update_states["current_read_holding_registers"][key] = deserialize_dict[key]


def _read_input_registers_live_update_deserialize(live_update_states, hex_response_array, deserialize_dict, logger):
    """This function deserializes the input response based on the information found in the live_update_states
        dictionary, calls the function that does the deserialization (deserialize()), which saves the result into
        a dictionary.
    Args:
        live_update_states(dict): State dictionary that contains the corresponding request and will contain deserialized
                            response.
        hex_response_array(list): Response bytes that are split into an array
        deserialize_dict(dict): A dictionary that contains the information about the request and response (both
                                serialized and unserialized).
    Returns:
    """
    modbus_response = hex_response_array[9:]
    start_add = hex(live_update_states["current_read_input_registers"]["current_request_from_gui"][0])

    deserialize_dict = read_input_registers_deserialize(modbus_response, start_add, deserialize_dict, logger)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in live_update_states["current_read_input_registers"]:
            live_update_states["current_read_input_registers"][key] = deserialize_dict[key]
