from datetime import datetime

from modbus_gui_app.communication.user_response_deserializer import *


def automatic_response_deserialize(state_manager, bytes_response):
    deserialize_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    is_without_errors = check_for_response_errors(deserialize_dict, hex_response_array)

    if is_without_errors is True:
        function_code = int(state_manager.current_coil_input_reg_states["currently_selected_function"])

        if function_code == 1:
            read_coils_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict)
        elif function_code == 2:
            read_discrete_inputs_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict)
        elif function_code == 2:
            read_holding_registers_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict)


def read_coils_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict):
    modbus_response = hex_response_array[9:]  # relevant parts are after the first 10 bytes of header data
    start_add = state_manager.current_coil_input_reg_states["current_read_coils"]["current_request_from_gui"][0]
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)
    deserialize_dict = read_coils_deserialize(modbus_response, start_add, deserialize_dict)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in state_manager.current_coil_input_reg_states["current_read_coils"]:
            state_manager.current_coil_input_reg_states["current_read_coils"][key] = deserialize_dict[key]


def read_discrete_inputs_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict):
    modbus_response = hex_response_array[9:]
    start_add = state_manager.current_coil_input_reg_states \
        ["current_read_discrete_inputs"]["current_request_from_gui"][0]
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)
    deserialize_dict = read_discrete_inputs_deserialize(modbus_response, start_add, deserialize_dict)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in state_manager.current_coil_input_reg_states["current_read_discrete_inputs"]:
            state_manager.current_coil_input_reg_states["current_read_discrete_inputs"][key] = \
                deserialize_dict[key]


def read_holding_registers_automatic_request_deserialize(state_manager, hex_response_array, deserialize_dict):
    modbus_response = hex_response_array[9:]
    start_add = state_manager.current_coil_input_reg_states \
        ["current_read_holding_registers"]["current_request_from_gui"][0]
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)
    deserialize_dict = read_holding_registers_deserialize(modbus_response, start_add, deserialize_dict)
    deserialize_dict["current_response_received_time"] = datetime.now()
    for key in deserialize_dict:
        if key in state_manager.current_coil_input_reg_states["current_read_holding_registers"]:
            state_manager.current_coil_input_reg_states["current_read_holding_registers"][key] = \
                deserialize_dict[key]
