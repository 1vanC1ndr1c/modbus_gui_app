from concurrent.futures.thread import ThreadPoolExecutor
import functools
import asyncio
import aiohttp

from modbus_gui_app.communication.deserializer import deserialize
from modbus_gui_app.communication.serializer import serialize


class ModbusCommunication:

    def __init__(self):
        self.communication_dict = {}
        self.tid = 1

    def set_current_tid(self):
        if self.tid > 9999:
            self.tid = 1
        else:
            self.tid = self.tid + 1

    def get_current_tid(self):
        return self.tid

    async def communicate_with_modbus(self, request_queue, response_queue, state_manager):
        session = aiohttp.ClientSession()
        ws = await session.ws_connect('ws://localhost:3456/ws')
        executor = ThreadPoolExecutor(1)

        async def ws_read_loop():
            while True:
                bytes_response = await ws.receive()
                if isinstance(bytes_response.data, bytes):
                    check_bytes = str(bytes_response.data.hex())
                    if check_bytes.startswith("0000"):
                        print("RESPONSE: received the dummy request that keeps the connection alive.")
                    else:
                        print("RESPONSE: ", bytes_response.data)
                        deserialized_dict = deserialize(bytes_response.data, state_manager)
                        response_queue.put(deserialized_dict)

        async def ws_write_loop():
            while True:
                dictionary = await asyncio.get_event_loop().run_in_executor(executor, functools.partial(
                    self.get_msg_from_queue, queue=request_queue))
                request_serialized = serialize(dictionary, state_manager, self.tid)
                print("REQUEST: ", request_serialized)
                self.set_current_tid()
                try:
                    await ws.send_bytes(request_serialized)
                except Exception:
                    pass

        async def ws_keep_connection_alive():
            while True:
                await asyncio.sleep(50)
                dummy_data = b'\x00\x00\x00\x00\x00\x06\x01\x01\x00\x00\x00\x01'
                await ws.send_bytes(dummy_data)
                print("REQUEST: send the dummy request that keeps the connection alive.")

        ws_keep_connection_alive_future = asyncio.ensure_future(ws_keep_connection_alive())
        ws_write_loop_future = asyncio.ensure_future(ws_write_loop())
        ws_read_loop_future = asyncio.ensure_future(ws_read_loop())

        await asyncio.wait([ws_read_loop_future, ws_write_loop_future, ws_keep_connection_alive_future],
                           return_when=asyncio.FIRST_COMPLETED)

        ws_read_loop_future.cancel()
        ws_write_loop_future.cancel()
        ws_keep_connection_alive_future.cancel()

        await ws.close()
        await session.close()

    def get_msg_from_queue(self, queue):
        request = queue.get()
        return request
