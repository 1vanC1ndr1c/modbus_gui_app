import asyncio
import aiohttp

from modbus_gui_app.communication.user_response_deserializer import user_response_deserialize
from modbus_gui_app.communication.user_request_serializer import user_request_serialize

from modbus_gui_app.communication.automatic_request_serializer import automatic_request_serialize
from modbus_gui_app.communication.automatic_response_deserializer import automatic_response_deserialize


class ModbusConnection:

    def __init__(self):
        self.communication_dict = {}
        self.tid = 0
        self._pending_responses = dict()

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def update_current_tid(self):
        if self.tid >= 9900:
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
        # print("REQUEST: Refresh GUI")
        automatic_request_serialize(self.state_manager)
        automatic_request = self.state_manager.current_coil_input_reg_states["current_request"]
        try:
            await self.ws.send_bytes(automatic_request)
        except Exception as e:
            print("AUTOMATIC REFRESH REQUEST ERROR: ", e)
        automatic_refresh_pending_response = asyncio.Future()
        automatic_request_tid = self.state_manager.current_coil_input_reg_states["current_tid"]
        self._pending_responses[automatic_request_tid] = automatic_refresh_pending_response
        await automatic_refresh_pending_response

    async def ws_read_loop(self):
        while True:
            bytes_response = await self.ws.receive()
            if isinstance(bytes_response.data, bytes):
                check_bytes = str(bytes_response.data.hex())
                if check_bytes.startswith("0000"):
                    automatic_request_tid = self.state_manager.current_coil_input_reg_states["current_tid"]
                    self._pending_responses[automatic_request_tid].set_result("Done.")
                elif check_bytes.startswith("99"):
                    automatic_response_deserialize(self.state_manager, bytes_response.data)
                    automatic_request_tid = self.state_manager.current_coil_input_reg_states["current_tid"]
                    # print("RESPONSE: Gui Refreshed.")
                    self._pending_responses[automatic_request_tid].set_result("Done.")
                else:
                    print("RESPONSE: ", bytes_response.data)
                    deserialized_dict = user_response_deserialize(bytes_response.data, self.state_manager)
                    self._pending_responses[self.get_current_tid()].set_result(deserialized_dict)
