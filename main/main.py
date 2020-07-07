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
    # save the last transaction ID
    last_tid = 0

    # TODO send this from GUI, one day
    unformed_request = '01 00 20 00 0C'
    function_code_address = '02'

    formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))

    formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))

    formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))

    formed_request, last_tid = form_request(unformed_request, function_code_address, last_tid)
    asyncio.get_event_loop().run_until_complete(communicate_with_modbus(formed_request))

