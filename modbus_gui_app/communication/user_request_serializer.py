def read_coils_serialize(start_addr, no_of_coils, unit_addr, tid):
    func_code = "01"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    no_of_coils = str(hex(no_of_coils))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + no_of_coils
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)
    communication_dict = _make_com_dict(tid, unit_addr, func_code, "Read Coils.", start_addr, no_of_coils, bytes_req)
    return bytes_req, communication_dict


def read_discrete_inputs_serialize(start_addr, input_count, unit_addr, tid):
    func_code = "02"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    input_count = str(hex(input_count))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + input_count
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Discrete Inputs."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, input_count, bytes_req)
    return bytes_req, communication_dict


def read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, tid):
    func_code = "03"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    h_regs_count = str(hex(h_regs_count))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + h_regs_count
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Holding Registers."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, h_regs_count, bytes_req)
    return bytes_req, communication_dict


def read_input_registers_serialize(start_addr, in_regs_count, unit_addr, tid):
    func_code = "04"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    in_regs_count = str(hex(in_regs_count))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + in_regs_count
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Read Input Registers."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, in_regs_count, bytes_req)
    return bytes_req, communication_dict


def write_single_coil_serialize(start_addr, coil_state, unit_addr, tid):
    func_code = "05"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')

    if coil_state == 0:
        modbus_request = func_code + start_addr + "ff" + "00"
    else:
        modbus_request = func_code + start_addr + "00" + "00"

    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Write Single Coil."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, str(coil_state), bytes_req)
    return bytes_req, communication_dict


def write_single_register_serialize(start_addr, reg_value, unit_addr, tid):
    func_code = "06"
    protocol = '0000'
    tid = str(hex(tid))[2:].rjust(4, '0')
    unit_addr = str(hex(unit_addr))[2:].rjust(2, '0')
    start_addr = str(hex(start_addr - 1))[2:].rjust(4, '0')
    reg_value = str(hex(reg_value))[2:].rjust(4, '0')

    modbus_request = func_code + start_addr + reg_value
    length = str(len(bytes.fromhex(modbus_request)) + 1).rjust(4, '0')
    bytes_req = bytes.fromhex(tid + protocol + length + unit_addr + modbus_request)

    name = "Write Single Register."
    communication_dict = _make_com_dict(tid, unit_addr, func_code, name, start_addr, reg_value, bytes_req)
    return bytes_req, communication_dict


def _make_com_dict(tid, unit_addr, func_code, req_name, start_addr, no_of_el, bytes_req):
    communication_dict = {
        "current_tid": int(tid, 16),
        "current_unit_address": str(int(unit_addr, 16)),
        "current_function_code": func_code,
        "current_request_name": req_name,
        "current_request_from_gui": [int(start_addr, 16) + 1, int(no_of_el, 16), int(unit_addr, 16), int(func_code)],
        "current_request_from_gui_is_valid": True,
        "current_request_from_gui_error_msg": "-",
        "current_request_serialized": bytes_req
    }
    return communication_dict
