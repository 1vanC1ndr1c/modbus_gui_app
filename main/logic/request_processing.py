import asyncio

from communication.modbus_communication import communicate_with_modbus

tid = 0

def process_request(unit_address, function_code, data):

    # #TODO replace this test data with arguments that are received

    # global tid
    # tid = 1
    # last_tid = 1
    # unformed_request = '01 00 20 00 0C'
    # function_code = '04'
    # #

    formed_request, last_tid = form_request(unit_address, function_code, data)
    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))

    # formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    # asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))
    #
    # formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    # asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))
    #
    # formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    # asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))
    #
    # formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
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
    for el in data:
        el = str(hex(el))[2:].rjust(4, '0')
        modbus_request = modbus_request + el

    length = len(bytes.fromhex(modbus_request)) + 1  # defined as length of bytes after the 'length' field
    length = str(length).rjust(4, '0')

    unit_address = str(unit_address).rjust(2, '0')
    full_request = new_tid + protocol + length + unit_address + modbus_request
    full_request = bytes.fromhex(full_request)

    return full_request, new_tid
