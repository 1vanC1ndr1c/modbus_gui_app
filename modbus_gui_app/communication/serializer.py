def serialize(dictionary, state_manager, tid):
    data = dictionary.get("current_request_from_gui")
    function_code = data[3]
    function_code = str(hex(function_code))[2:].rjust(2, '0')
    dictionary["current_tid"] = tid

    if function_code == "01":
        full_request = read_coils_serialize(function_code, data, state_manager, dictionary)
        return full_request
    elif function_code == "02":
        full_request = read_discrete_inputs_serialize(function_code, data, state_manager, dictionary)
        return full_request
    elif function_code == "03":
        full_request = read_holding_registers_serialize(function_code, data, state_manager, dictionary)
        return full_request
    elif function_code == "04":
        full_request = read_input_registers_serialize(function_code, data, state_manager, dictionary)
        return full_request
    elif function_code == "05":
        full_request = write_single_coil_serialize(function_code, data, state_manager, dictionary)
        return full_request
    elif function_code == "06":
        full_request = write_single_register_serialize(function_code, data, state_manager, dictionary)
        return full_request
    else:
        state_manager.set_current_request_name("Unknown Request.")
        return b'0'


def read_coils_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Read Coils.")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    no_of_coils = str(hex(data[1]))[2:].rjust(4, '0')

    modbus_request = function_code + ''
    modbus_request = modbus_request + start_add + no_of_coils

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def read_discrete_inputs_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Read Discrete Inputs .")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    no_of_discrete_inputs = str(hex(data[1]))[2:].rjust(4, '0')

    modbus_request = function_code + ''
    modbus_request = modbus_request + start_add + no_of_discrete_inputs

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def read_holding_registers_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Read Holding Registers.")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    no_of_holding_registers = str(hex(data[1]))[2:].rjust(4, '0')

    modbus_request = function_code + ''
    modbus_request = modbus_request + start_add + no_of_holding_registers

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def read_input_registers_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Read Input Registers.")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    no_of_input_registers = str(hex(data[1]))[2:].rjust(4, '0')

    modbus_request = function_code + ''
    modbus_request = modbus_request + start_add + no_of_input_registers

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def write_single_coil_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Write Single Coil.")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    state_select = data[1]
    modbus_request = function_code + ''
    if state_select == 0:
        modbus_request = modbus_request + start_add + "ff" + "00"
    else:
        modbus_request = modbus_request + start_add + "00" + "00"

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def write_single_register_serialize(function_code, data, state_manager, dictionary):
    state_manager.set_current_request_name("Write Single Register.")

    new_tid, protocol, unit_address, start_add = \
        get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code)

    reg_val = data[1]
    reg_val = str(hex(reg_val))[2:].rjust(4, '0')
    modbus_request = function_code + ''
    modbus_request = modbus_request + start_add + reg_val

    serialized_request = generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager)
    return serialized_request


def get_tid_protocol_unitaddr_startaddr(dictionary, data, state_manager, function_code):
    new_tid = dictionary.get("current_tid")
    new_tid = str(new_tid).rjust(4, '0')
    protocol = '0000'
    unit_address = data[2]
    unit_address = str(unit_address).rjust(2, '0')
    state_manager.set_current_unit_address(str(unit_address))
    state_manager.set_current_function_code(str(function_code))
    start_add = data[0]
    start_add = start_add - 1
    start_add = str(hex(start_add))[2:].rjust(4, '0')

    return new_tid, protocol, unit_address, start_add


def generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager):
    length = len(bytes.fromhex(modbus_request)) + 1
    length = str(length).rjust(4, '0')

    serialized_request = new_tid + protocol + length + unit_address + modbus_request
    serialized_request = bytes.fromhex(serialized_request)

    state_manager.set_current_request_serialized(serialized_request)
    return serialized_request
