import os
import asyncio
import aiohttp.web
import contextlib
import json
import sys
import subprocess
import socket
from multiprocessing import Process
import websocket


def form_request(modbus_request, unit_address, used_tids_list, latest_tid):
    # reset the tid if the maximum is reached
    if latest_tid == 9999:
        latest_tid = 0
    while True:
        # new transaction ID is the previous one incremented by one
        latest_tid = latest_tid + 1
        # check if the ID is already in use
        if latest_tid not in used_tids_list:
            # if not, mark it as currently used
            used_tids_list.append(latest_tid)
            break

    tid = str(latest_tid).rjust(4, '0')  # transaction ID formed into 2 bytes
    protocol = '00 00'  # doesn't change
    length = len(bytes.fromhex(modbus_request)) + 1 # defined as length of bytes after the 'length' field
    length = str(length).rjust(4, '0')

    # default test data
    # unit_address = '02'
    # tid = '00 05' # test TID
    # modbus_request = '01 00 20 00 0C' test request
    # protocol = '00 00'  # doesn't change
    # length = '00 06'
    # return bytes.fromhex('00 05 00 00 00 06 02 01 00 20 00 0C')

    return (bytes.fromhex(tid + protocol + length + unit_address + modbus_request)), latest_tid, used_tids_list


async def communicate_with_modbus(request):
    session = aiohttp.ClientSession()
    ws = await session.ws_connect('ws://localhost:3456/ws')
    await ws.send_bytes(request)

    modbus_response = "No response."

    msg = await ws.receive()
    if isinstance(msg.data, bytes):
        modbus_response = msg.data

    msg = await ws.receive()
    if isinstance(msg.data, bytes):
        modbus_response = msg.data

    if modbus_response == "No response.":
        print("No response.")

    print(modbus_response)

    await ws.close()
    await session.close()


if __name__ == '__main__':
    # list of transaction IDs
    currently_used_tids = []
    # save the last transaction ID
    last_tid = 0

    unformed_request = '01 00 20 00 0C'
    function_code_address = '02'
    formed_request, new_last_tid, new_tid_list = form_request(unformed_request,function_code_address, currently_used_tids, last_tid)
    formed_request, new_last_tid, new_tid_list = form_request(unformed_request,function_code_address, currently_used_tids, last_tid)
    formed_request, new_last_tid, new_tid_list = form_request(unformed_request,function_code_address, currently_used_tids, last_tid)
    formed_request, new_last_tid, new_tid_list = form_request(unformed_request,function_code_address, currently_used_tids, last_tid)
    formed_request, new_last_tid, new_tid_list = form_request(unformed_request,function_code_address, currently_used_tids, last_tid)

    currently_used_tids = new_tid_list
    last_tid = new_last_tid

    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))
