import asyncio

from communication.modbus_communication import communicate_with_modbus

tid = 0
# response = -1
response = b'\x00\x01\x00\x00\x00\x05\x02\x01\x02\x80\x02'


def process_request(unit_address, function_code, data):
    formed_request, last_tid = form_request(unit_address, function_code, data)
    # asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))


# TID (global), Protocol(Always the same), Length(Needs to be calculated), Unit Address, MSG
def form_request(unit_address, function_code, data):
    # reset the tid if the maximum is reached
    global tid
    if tid == 9999:
        tid = 0
    tid = tid + 1
    new_tid = str(tid).rjust(4, '0')  # transaction ID formed into 2 bytes

    protocol = '0000'  # doesn't change

    function_code = str(hex(function_code))[2:].rjust(2, '0')
    modbus_request = function_code + ''

    if function_code == '01':
        start_add = data[0]
        start_add = start_add - 1
        start_add = str(hex(start_add))[2:].rjust(4, '0')
        no_of_coils = data[1]
        no_of_coils = str(hex(no_of_coils))[2:].rjust(4, '0')
        modbus_request = modbus_request + start_add + no_of_coils

    length = len(bytes.fromhex(modbus_request)) + 1  # defined as length of bytes after the 'length' field
    length = str(length).rjust(4, '0')

    unit_address = str(unit_address).rjust(2, '0')
    full_request = new_tid + protocol + length + unit_address + modbus_request
    full_request = bytes.fromhex(full_request)

    return full_request, new_tid
    # return b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16', 1    # test data


def set_response(r):
    global response
    response = r


def get_response():
    global response
    return response
