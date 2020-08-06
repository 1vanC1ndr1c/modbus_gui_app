def _user_request_serialize(state_dict, state_manager, tid):
    req_dict = state_dict.get("current_request_from_gui")
    func_code = req_dict[3]
    func_code = str(hex(func_code))[2:].rjust(2, '0')
    state_dict["current_tid"] = tid

    if func_code == "01":
        bytes_req = _read_coils_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    elif func_code == "02":
        bytes_req = _read_discrete_inputs_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    elif func_code == "03":
        bytes_req = _read_holding_registers_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    elif func_code == "04":
        bytes_req = _read_input_registers_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    elif func_code == "05":
        bytes_req = _write_single_coil_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    elif func_code == "06":
        bytes_req = _write_single_register_serialize(func_code, req_dict, state_manager, state_dict)
        return bytes_req
    else:
        state_manager.set_current_request_name("Unknown Request.")
        return b'0'


def _read_coils_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Read Coils.")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    no_of_coils = str(hex(req_dict[1]))[2:].rjust(4, '0')
    modbus_request = func_code + ''
    modbus_request = modbus_request + start_addr + no_of_coils

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _read_discrete_inputs_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Read Discrete Inputs .")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    no_of_discrete_inputs = str(hex(req_dict[1]))[2:].rjust(4, '0')
    modbus_request = func_code + ''
    modbus_request = modbus_request + start_addr + no_of_discrete_inputs

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _read_holding_registers_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Read Holding Registers.")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    no_of_holding_registers = str(hex(req_dict[1]))[2:].rjust(4, '0')
    modbus_request = func_code + ''
    modbus_request = modbus_request + start_addr + no_of_holding_registers

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _read_input_registers_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Read Input Registers.")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    no_of_input_registers = str(hex(req_dict[1]))[2:].rjust(4, '0')
    modbus_request = func_code + ''
    modbus_request = modbus_request + start_addr + no_of_input_registers

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _write_single_coil_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Write Single Coil.")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    modbus_request = func_code + ''
    on_off_select = req_dict[1]
    if on_off_select == 0:
        modbus_request = modbus_request + start_addr + "ff" + "00"
    else:
        modbus_request = modbus_request + start_addr + "00" + "00"

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _write_single_register_serialize(func_code, req_dict, state_manager, state_dict):
    state_manager.set_current_request_name("Write Single Register.")

    new_tid, protocol, unit_addr, start_addr = _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, func_code)
    reg_val = req_dict[1]
    reg_val = str(hex(reg_val))[2:].rjust(4, '0')
    modbus_request = func_code + ''
    modbus_request = modbus_request + start_addr + reg_val

    bytes_req = _generate_serialized_request(modbus_request, new_tid, protocol, unit_addr, state_manager)
    return bytes_req


def _get_tid_prot_uddr_saddr(state_dict, req_dict, state_manager, function_code):
    new_tid = state_dict.get("current_tid")
    new_tid = str(new_tid).rjust(4, '0')
    protocol = '0000'
    unit_address = req_dict[2]
    unit_address = str(unit_address).rjust(2, '0')
    state_manager.set_current_unit_address(str(unit_address))
    state_manager.set_current_function_code(str(function_code))
    start_add = req_dict[0]
    start_add = start_add - 1
    start_add = str(hex(start_add))[2:].rjust(4, '0')

    return new_tid, protocol, unit_address, start_add


def _generate_serialized_request(modbus_request, new_tid, protocol, unit_address, state_manager):
    length = len(bytes.fromhex(modbus_request)) + 1
    length = str(length).rjust(4, '0')

    bytes_req = new_tid + protocol + length + unit_address + modbus_request
    bytes_req = bytes.fromhex(bytes_req)

    state_manager.set_current_request_serialized(bytes_req)
    return bytes_req
