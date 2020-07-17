def deserialize(bytes_response, state_manager):
    deserialize_dict = {}

    deserialize_dict["current_response_serialized"] = bytes_response
    deserialize_dict["current_response_is_valid"] = True
    try:
        if str(bytes_response).split('\\')[8].startswith('x8'):  # check for errors in the response
            err_msg = str(bytes_response).split('\\')[9]
            err_msg = err_msg.replace("\'", "")
            err_msg = err_msg.replace("\"", "")
            err_msg = err_msg.replace("x", "")
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
            return deserialize_dict
    except:
        deserialize_dict["current_response_is_valid"] = False
        deserialize_dict["current_response_err_msg"] = "Error with the request processing!"
        deserialize_dict["current_response_serialized"] = "/"
        return deserialize_dict

    function_code = state_manager.get_dict()["current_request_from_gui"][3]

    modbus_response = str(bytes_response).split("\\x")
    modbus_response = modbus_response[10:]
    start_add = state_manager.get_dict()["current_request_from_gui"][0]
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)

    if function_code == 1 or function_code == 2:

        binary_data = ""
        for r in modbus_response:
            r = r.replace("\'", "")
            r = r.replace("\"", "")
            scale = 16
            num_of_bits = 8
            # get the reversed the bits
            bin_data_byte = bin(int(r, scale))[2:].zfill(num_of_bits)
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
            indices = "/"
        deserialize_dict["current_response_returned_values"] = indices
        deserialize_dict["current_response_err_msg"] = "/"
        return deserialize_dict

    elif function_code == 3 or function_code == 4:

        values = []
        for i in range(0, len(modbus_response), 2):
            try:
                values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
            except:
                pass
        if len(values) == 0:
            values = "/"
            deserialize_dict["current_response_returned_values"] = values
            deserialize_dict["current_response_err_msg"] = "/"
            return deserialize_dict

        location_and_value = []
        for i, val in enumerate(values):
            location = i + int(start_add, 16)
            location = hex(location)
            location_and_value.append([location, val])
        deserialize_dict["current_response_err_msg"] = "/"
        deserialize_dict["current_response_returned_values"] = location_and_value
        return deserialize_dict

    elif function_code == 5 or function_code == 6:
        deserialize_dict["current_response_err_msg"] = "/"
        deserialize_dict["current_response_returned_values"] = str(bytes_response)
        return deserialize_dict
