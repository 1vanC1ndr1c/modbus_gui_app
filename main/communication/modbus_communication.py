import asyncio
import functools
from concurrent.futures.thread import ThreadPoolExecutor
import aiohttp

import request_processing


async def communicate_with_modbus(request_queue, response_queue):
    session = aiohttp.ClientSession()
    ws = await session.ws_connect('ws://localhost:3456/ws')
    executor = ThreadPoolExecutor(1)

    async def ws_read_loop():
        while True:
            response = await ws.receive()
            if isinstance(response.data, bytes):
                response_queue.put(response.data)
                print("RESPONSE: ", response.data)

    async def ws_write_loop():
        while True:
            request = await asyncio.get_event_loop().run_in_executor(executor, functools.partial(
                get_msg_from_queue, queue=request_queue))
            print("REQUEST: ", request)
            try:
                await ws.send_bytes(request)
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
