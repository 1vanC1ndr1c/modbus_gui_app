def serialize(dict, state_manager):
    data = dict.get("current_request_from_gui")

    new_tid = dict.get("current_tid")
    new_tid = str(new_tid).rjust(4, '0')  # transaction ID formed into 2 bytes
    protocol = '0000'  # doesn't change
    unit_address = data[2]

    function_code = data[3]
    function_code = str(hex(function_code))[2:].rjust(2, '0')
    modbus_request = function_code + ''

    if function_code == '01' or function_code == '02' or function_code == '03' or function_code == '04':
        start_add = data[0]
        start_add = start_add - 1
        start_add = str(hex(start_add))[2:].rjust(4, '0')
        no_of_coils = data[1]
        no_of_coils = str(hex(no_of_coils))[2:].rjust(4, '0')
        modbus_request = modbus_request + start_add + no_of_coils

    elif function_code == '05':
        start_add = data[0]
        start_add = start_add - 1
        start_add = str(hex(start_add))[2:].rjust(4, '0')
        state_select = data[1]
        if state_select == 0:
            modbus_request = modbus_request + start_add + "ff" + "00"
        else:
            modbus_request = modbus_request + start_add + "00" + "00"

    elif function_code == '06':
        start_add = data[0]
        start_add = start_add - 1
        start_add = str(hex(start_add))[2:].rjust(4, '0')
        reg_val = data[1]
        reg_val = str(hex(reg_val))[2:].rjust(4, '0')
        modbus_request = modbus_request + start_add + reg_val

    length = len(bytes.fromhex(modbus_request)) + 1  # defined as length of bytes after the 'length' field
    length = str(length).rjust(4, '0')

    unit_address = str(unit_address).rjust(2, '0')
    serialized_request = new_tid + protocol + length + unit_address + modbus_request
    serialized_request = bytes.fromhex(serialized_request)

    state_manager.set_current_request_serialized(serialized_request)
    return serialized_request
    # return b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16'    # test data
