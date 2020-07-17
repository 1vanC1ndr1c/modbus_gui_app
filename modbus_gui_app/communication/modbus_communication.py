from concurrent.futures.thread import ThreadPoolExecutor
import functools
import asyncio
import aiohttp

from modbus_gui_app.communication.deserializer import deserialize
from modbus_gui_app.communication.serializer import serialize


async def communicate_with_modbus(request_queue, response_queue, state_manager):
    session = aiohttp.ClientSession()
    ws = await session.ws_connect('ws://localhost:3456/ws')
    executor = ThreadPoolExecutor(1)

    async def ws_read_loop():
        while True:
            bytes_response = await ws.receive()
            if isinstance(bytes_response.data, bytes):
                print("RESPONSE: ", bytes_response.data)
                deserialized_dict = deserialize(bytes_response.data, state_manager)
                response_queue.put(deserialized_dict)

    async def ws_write_loop():
        while True:
            dictionary = await asyncio.get_event_loop().run_in_executor(executor, functools.partial(
                get_msg_from_queue, queue=request_queue))
            request_serialized = serialize(dictionary, state_manager)
            print("REQUEST: ", request_serialized)
            try:
                await ws.send_bytes(request_serialized)
            except Exception:
                pass

    ws_write_loop_future = asyncio.ensure_future(ws_write_loop())
    ws_read_loop_future = asyncio.ensure_future(ws_read_loop())

    await asyncio.wait([ws_read_loop_future, ws_write_loop_future], return_when=asyncio.FIRST_COMPLETED)

    ws_read_loop_future.cancel()
    ws_write_loop_future.cancel()

    await ws.close()
    await session.close()


def get_msg_from_queue(queue):
    request = queue.get()
    return request
