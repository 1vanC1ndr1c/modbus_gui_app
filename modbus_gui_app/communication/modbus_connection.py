from concurrent.futures.thread import ThreadPoolExecutor
import functools
import asyncio
import aiohttp

from modbus_gui_app.communication.deserializer import deserialize
from modbus_gui_app.communication.serializer import serialize


class ModbusConnection:

    def __init__(self):
        self.communication_dict = {}
        self.tid = 0
        self._pending_responses = dict()

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def update_current_tid(self):
        if self.tid > 9999:
            self.tid = 1
        else:
            self.tid = self.tid + 1

    def get_current_tid(self):
        return self.tid

    async def communicate_with_modbus(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect('ws://localhost:3456/ws')

    async def ws_write(self, validated_request):
        print("WRITING")
        self.update_current_tid()
        request_serialized = serialize(validated_request, self.state_manager, self.tid)
        print("REQUEST: ", request_serialized)
        try:
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            print("REQUEST ERROR: ", e)
        pending_response = asyncio.Future()
        self._pending_responses[self.get_current_tid()] = pending_response
        return await pending_response

    async def ws_read_loop(self):
        while True:
            bytes_response = await self.ws.receive()
            if isinstance(bytes_response.data, bytes):
                check_bytes = str(bytes_response.data.hex())
                if check_bytes.startswith("0000"):
                    print("RESPONSE: received the dummy request that keeps the connection alive.")
                else:
                    print("RESPONSE: ", bytes_response.data)
                    deserialized_dict = deserialize(bytes_response.data, self.state_manager)
                    self._pending_responses[self.get_current_tid()].set_result(deserialized_dict)

    # async def ws_keep_connection_alive(self):
    #     return
        # while True:
        #     await asyncio.sleep(50)
        #     dummy_data = b'\x00\x00\x00\x00\x00\x06\x01\x01\x00\x00\x00\x01'
        #     await self.ws.send_bytes(dummy_data)
        #     print("REQUEST: send the dummy request that keeps the connection alive.")