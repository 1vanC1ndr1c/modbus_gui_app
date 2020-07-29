import asyncio
import aiohttp

from modbus_gui_app.communication.user_response_deserializer import user_response_deserialize
from modbus_gui_app.communication.user_request_serializer import user_request_serialize

from modbus_gui_app.communication.automatic_request_serializer import automatic_request_serialize


class ModbusConnection:

    def __init__(self):
        self.communication_dict = {}
        self.tid = 0
        self._pending_responses = dict()

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def update_current_tid(self):
        if self.tid > 9900:
            self.tid = 1
        else:
            self.tid = self.tid + 1

    def get_current_tid(self):
        return self.tid

    async def connect_with_modbus(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect('ws://localhost:3456/ws')

    async def ws_write(self, validated_request):
        self.update_current_tid()
        request_serialized = user_request_serialize(validated_request, self.state_manager, self.tid)
        print("REQUEST: ", request_serialized)
        try:
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            print("REQUEST ERROR: ", e)
        pending_response = asyncio.Future()
        self._pending_responses[self.get_current_tid()] = pending_response
        return await pending_response

    async def ws_refresh(self):
        print("REGUEST: Refresh GUI")
        # TODO get the old request from the dictionary
        automatic_request_serialize(self.state_manager)
        # TODO form the new request
        refresh_request = "NEW REQUEST"
        # await self.ws.send_bytes(refresh_request)
        # TODO get the request from the dictionary
        temp_data = b'\x00\x00\x00\x00\x00\x06\x01\x01\x00\x00\x00\x01'
        await self.ws.send_bytes(temp_data)
        current_refresh_function = "GET FROM DICT"
        # print("REQUEST: refresh the current state which is {}.".format(current_refresh_function))

    async def ws_read_loop(self):
        while True:
            bytes_response = await self.ws.receive()
            if isinstance(bytes_response.data, bytes):
                check_bytes = str(bytes_response.data.hex())
                if check_bytes.startswith("0000"):
                    print("RESPONSE: Refresh GUI.")
                else:
                    print("RESPONSE: ", bytes_response.data)
                    deserialized_dict = user_response_deserialize(bytes_response.data, self.state_manager)
                    self._pending_responses[self.get_current_tid()].set_result(deserialized_dict)
