import re


def deserialize(bytes_response, state_manager):
    deserialize_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    hex_response_array = re.findall('..', str(bytes_response.hex()))  # convert the byte response into string(hex)

    is_without_errors = check_for_response_errors(deserialize_dict, hex_response_array)
    if is_without_errors is False:
        return deserialize_dict

    function_code = state_manager.get_dict()["current_request_from_gui"][3]
    modbus_response = hex_response_array[9:]  # relevant parts are after the first 10 bytes of header data
    start_add = state_manager.get_dict()["current_request_from_gui"][0]
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)

    if function_code == 1:
        return read_coils_deserialize(modbus_response, start_add, deserialize_dict)
    elif function_code == 2:
        return read_discrete_inputs_deserialize(modbus_response, start_add, deserialize_dict)
    elif function_code == 3:
        return read_holding_registers_deserialize(modbus_response, start_add, deserialize_dict)
    elif function_code == 4:
        return read_input_registers_deserialize(modbus_response, start_add, deserialize_dict)
    elif function_code == 5:
        return write_single_coil_deserialize(deserialize_dict, bytes_response)
    elif function_code == 6:
        return write_single_register_deserialize(deserialize_dict, bytes_response)
    else:
        deserialize_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": False,
                            "current_response_err_msg": "Unknown Request."}
        return deserialize_dict


def read_coils_deserialize(modbus_response, start_add, deserialize_dict):
    binary_data = ""
    for byte in modbus_response:
        scale = 16
        num_of_bits = 8
        bin_data_byte = bin(int(byte, scale))[2:].zfill(num_of_bits)  # get the reversed the bits
        bin_data_byte = str(bin_data_byte)
        bin_data_byte = bin_data_byte[len(bin_data_byte)::-1]
        binary_data = binary_data + bin_data_byte

    indices = []
    for i, bit in enumerate(binary_data):
        if bit == '1':
            res = i + int(start_add, 16)
            res = hex(res)
            indices.append(res)
    if len(indices) == 0:
        indices = "-"

    deserialize_dict["current_response_returned_values"] = indices
    deserialize_dict["current_response_err_msg"] = "-"
    return deserialize_dict


def read_discrete_inputs_deserialize(modbus_response, start_add, deserialize_dict):
    binary_data = ""
    for byte in modbus_response:
        scale = 16
        num_of_bits = 8
        bin_data_byte = bin(int(byte, scale))[2:].zfill(num_of_bits)  # get the reversed the bits
        bin_data_byte = str(bin_data_byte)
        bin_data_byte = bin_data_byte[len(bin_data_byte)::-1]
        binary_data = binary_data + bin_data_byte

    indices = []
    for i, bit in enumerate(binary_data):
        if bit == '1':
            res = i + int(start_add, 16)
            res = hex(res)
            indices.append(res)
    if len(indices) == 0:
        indices = "-"

    deserialize_dict["current_response_returned_values"] = indices
    deserialize_dict["current_response_err_msg"] = "-"
    return deserialize_dict


def read_holding_registers_deserialize(modbus_response, start_add, deserialize_dict):
    values = []
    for i in range(0, len(modbus_response), 2):
        try:
            values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
        except Exception as e:
            print(e)
            pass
    if len(values) == 0:
        values = "-"
        deserialize_dict["current_response_returned_values"] = values
        deserialize_dict["current_response_err_msg"] = "-"
        return deserialize_dict

    location_and_value = []
    for i, val in enumerate(values):
        location = i + int(start_add, 16)
        location = hex(location)
        if str(val) != "0000":
            location_and_value.append([location, val])
    if len(location_and_value) == 0:
        location_and_value = "-"
    deserialize_dict["current_response_err_msg"] = "-"
    deserialize_dict["current_response_returned_values"] = location_and_value
    return deserialize_dict


def read_input_registers_deserialize(modbus_response, start_add, deserialize_dict):
    values = []
    for i in range(0, len(modbus_response), 2):
        try:
            values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
        except Exception as e:
            print(e)
            pass
    if len(values) == 0:
        values = "-"
        deserialize_dict["current_response_returned_values"] = values
        deserialize_dict["current_response_err_msg"] = "-"
        return deserialize_dict

    location_and_value = []
    for i, val in enumerate(values):
        location = i + int(start_add, 16)
        location = hex(location)
        if str(val) != "0000":
            location_and_value.append([location, val])
    if len(location_and_value) == 0:
        location_and_value = "-"
    deserialize_dict["current_response_err_msg"] = "-"
    deserialize_dict["current_response_returned_values"] = location_and_value
    return deserialize_dict


def write_single_coil_deserialize(deserialize_dict, bytes_response):
    deserialize_dict["current_response_err_msg"] = "-"
    deserialize_dict["current_response_returned_values"] = str(bytes_response)
    return deserialize_dict


def write_single_register_deserialize(deserialize_dict, bytes_response):
    deserialize_dict["current_response_err_msg"] = "-"
    deserialize_dict["current_response_returned_values"] = str(bytes_response)
    return deserialize_dict


def check_for_response_errors(deserialize_dict, hex_response_array):
    try:
        if hex_response_array[7].startswith('8'):
            err_msg = str(hex_response_array[8])
            if err_msg == "01":
                err_msg = "ERROR: Illegal function"
            elif err_msg == "02":
                err_msg = "ERROR: Illegal data address"
            elif err_msg == "03":
                err_msg = "ERROR: Illegal data value"
            else:
                err_msg = "ERROR: Slave device failure"
            deserialize_dict["current_response_is_valid"] = False
            deserialize_dict["current_response_err_msg"] = err_msg
            return False
    except:
        deserialize_dict["current_response_is_valid"] = False
        deserialize_dict["current_response_err_msg"] = "Error with the request processing!"
        deserialize_dict["current_response_serialized"] = "-"
        return False
    return True
