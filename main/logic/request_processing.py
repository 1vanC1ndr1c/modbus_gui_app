import asyncio

from communication.modbus_communication import communicate_with_modbus


def process_request():

    #TODO replace this test data with arguments that are received
    last_tid = 1
    unformed_request = '01 00 20 00 0C'
    function_code_address = '02'

    formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
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


def form_request(modbus_request, unit_address, latest_tid):
    # reset the tid if the maximum is reached
    if latest_tid == 9999:
        latest_tid = 0

    latest_tid = latest_tid + 1

    tid = str(latest_tid).rjust(4, '0')  # transaction ID formed into 2 bytes
    protocol = '00 00'  # doesn't change
    length = len(bytes.fromhex(modbus_request)) + 1  # defined as length of bytes after the 'length' field
    length = str(length).rjust(4, '0')

    return (bytes.fromhex(tid + protocol + length + unit_address + modbus_request)), latest_tid
