import logging
import re



def response_deserialize(bytes_response, communication_dictionary):
    """ This function deserializes chooses the correct deserialization function (based on the function code).

    Args:
        bytes_response(bytes): Received response that needs to be deserialized.
        communication_dictionary(dict): A dictionary that contains the information about the request that prompted
                                        this particular response.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.

    """
    logger = logging.getLogger()

    response_dict = {"current_response_serialized": bytes_response, "current_response_is_valid": True}

    hex_response_array = re.findall('..', str(bytes_response.hex()))

    is_valid = check_for_response_errors(response_dict, hex_response_array, logger)
    if is_valid is False:
        return response_dict

    tid = ''.join(hex_response_array[:2])
    response_dict["response_tid"] = tid
    func_code = communication_dictionary["current_request_from_gui"][3]
    modbus_resp = hex_response_array[9:]
    start_addr = communication_dictionary["current_request_from_gui"][0]
    start_addr = hex(start_addr)

    if func_code == 1:
        return read_coils_deserialize(modbus_resp, start_addr, response_dict)
    elif func_code == 2:
        return read_discrete_inputs_deserialize(modbus_resp, start_addr, response_dict)
    elif func_code == 3:
        return read_holding_registers_deserialize(modbus_resp, start_addr, response_dict, logger)
    elif func_code == 4:
        return read_input_registers_deserialize(modbus_resp, start_addr, response_dict, logger)
    elif func_code == 5:
        return write_single_coil_deserialize(response_dict, bytes_response)
    elif func_code == 6:
        return write_single_register_deserialize(response_dict, bytes_response)
    else:
        response_dict = {
            "current_response_serialized": bytes_response,
            "current_response_is_valid": False,
            "current_response_err_msg": "Unknown Request."
        }
        return response_dict


def read_coils_deserialize(modbus_response, start_addr, response_dict):
    """This function deserializes the input data into information that is stored in a dictionary.

    Args:
        modbus_response(byte): The part of the request that contains information about the request result.
        start_addr(hex): The address from which the reading starts.
        response_dict(dict): A dictionary that is used to save the deserialized data.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.

    """
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
            res = i + int(start_addr, 16)
            res = hex(res)
            indices.append(res)
    if len(indices) == 0:
        indices = "-"
    response_dict["current_response_returned_values"] = indices
    response_dict["current_response_err_msg"] = "-"
    return response_dict


def read_discrete_inputs_deserialize(modbus_response, start_add, response_dict):
    """This function deserializes the input data into information that is stored in a dictionary.

    Args:
        modbus_response(byte): The part of the request that contains information about the request result.
        start_add(hex): The address from which the reading starts.
        response_dict(dict): A dictionary that is used to save the deserialized data.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.

    """
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

    response_dict["current_response_returned_values"] = indices
    response_dict["current_response_err_msg"] = "-"
    return response_dict


def read_holding_registers_deserialize(modbus_response, start_add, response_dict, logger):
    """This function deserializes the input data into information that is stored in a dictionary.
       Logs an error if one occurs.

    Args:
        modbus_response(byte): The part of the request that contains information about the request result.
        start_add(hex): The address from which the reading starts.
        response_dict(dict): A dictionary that is used to save the deserialized data.
        logger(logging.logger): A logger that saves any raised exceptions.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.

    """
    values = []
    for i in range(0, len(modbus_response), 2):
        try:
            values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
        except:
            logger.exception("RESPONSE DESERIALIZER: Deserialization Error: \n")
            pass
    if len(values) == 0:
        values = "-"
        response_dict["current_response_returned_values"] = values
        response_dict["current_response_err_msg"] = "-"
        return response_dict

    location_and_value = []

    for i, val in enumerate(values):
        location = i + int(start_add, 16)
        location = hex(location)
        if str(val) != "0000":
            location_and_value.append([location, val])
    if len(location_and_value) == 0:
        location_and_value = "-"

    response_dict["current_response_err_msg"] = "-"
    response_dict["current_response_returned_values"] = location_and_value
    return response_dict


def read_input_registers_deserialize(modbus_response, start_add, response_dict, logger):
    """This function deserializes the input data into information that is stored in a dictionary.
       Logs an error if one occurs.

    Args:
        modbus_response: The part of the request that contains information about the request result.
        start_add: The address from which the reading starts.
        response_dict: A dictionary that is used to save the deserialized data.
        logger(logging.logger): A logger that saves any raised exceptions.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.

    """
    values = []
    for i in range(0, len(modbus_response), 2):
        try:
            values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
        except:
            logger.exception("RESPONSE DESERIALIZER: Deserialization Error: \n")
            pass
    if len(values) == 0:
        values = "-"
        response_dict["current_response_returned_values"] = values
        response_dict["current_response_err_msg"] = "-"
        return response_dict

    location_and_value = []
    for i, val in enumerate(values):
        location = i + int(start_add, 16)
        location = hex(location)
        if str(val) != "0000":
            location_and_value.append([location, val])
    if len(location_and_value) == 0:
        location_and_value = "-"

    response_dict["current_response_err_msg"] = "-"
    response_dict["current_response_returned_values"] = location_and_value
    return response_dict


def write_single_coil_deserialize(response_dict, bytes_response):
    """This function deserializes the input data into information that is stored in a dictionary.

    Args:
        bytes_response: The part of the request that contains information about the request result..
        response_dict: A dictionary that is used to save the deserialized data.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.
    """
    response_dict["current_response_err_msg"] = "-"
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    response_dict["current_response_returned_values"] = hex_response_array
    return response_dict


def write_single_register_deserialize(response_dict, bytes_response):
    """This function deserializes the input data into information that is stored in a dictionary.

    Args:
        bytes_response: The part of the request that contains information about the request result..
        response_dict: A dictionary that is used to save the deserialized data.

    Returns:
        dict: A dictionary that contains the information about the deserialized response.
    """
    response_dict["current_response_err_msg"] = "-"
    hex_response_array = re.findall('..', str(bytes_response.hex()))
    response_dict["current_response_returned_values"] = hex_response_array
    return response_dict


def check_for_response_errors(response_dict, hex_response_array, logger):
    """This function deserialized the response and checks whether it contains any error messages.

    Args:
        response_dict: A dictionary which is used to save the error checking result and the error(if there is any).
        hex_response_array: The byte
        logger(logging.logger): A logger that saves any raised exceptions.

    Returns:
        boolean: True if valid, False otherwise.

    """
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
            response_dict["current_response_is_valid"] = False
            response_dict["current_response_err_msg"] = err_msg
            return False
    except:
        logger.exception("RESPONSE DESERIALIZER: Error when checking for errors: \n")
        response_dict["current_response_is_valid"] = False
        response_dict["current_response_err_msg"] = "Error with the request processing!"
        response_dict["current_response_serialized"] = "-"
        return False
    return True
