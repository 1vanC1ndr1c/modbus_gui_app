import aiohttp

import request_processing


async def communicate_with_modbus(request):
    session = aiohttp.ClientSession()
    ws = await session.ws_connect('ws://localhost:3456/ws')
    await ws.send_bytes(request)

    modbus_response = "No response."

    print("REQUEST=", str(request))

    msg = await ws.receive()
    if isinstance(msg.data, bytes):
        modbus_response = msg.data

    msg = await ws.receive()
    if isinstance(msg.data, bytes):
        modbus_response = msg.data

    if modbus_response == "No response.":
        print("No response.")

    print("RESPONSE=", modbus_response)

    await ws.close()
    await session.close()

    request_processing.set_response(modbus_response)
