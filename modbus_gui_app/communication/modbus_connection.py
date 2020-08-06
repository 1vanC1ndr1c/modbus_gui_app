import asyncio

import aiohttp

from modbus_gui_app.communication.live_update_req_serializer import _automatic_request_serialize
from modbus_gui_app.communication.live_update_resp_deserializer import _live_update_response_deserialize
from modbus_gui_app.communication.user_request_serializer import _user_request_serialize
from modbus_gui_app.communication.user_response_deserializer import _user_response_deserialize


class ModbusConnection:

    def __init__(self):
        self._communication_dict = {}
        self._tid = 0
        self._pending_responses = {}
        self._state_manager = None
        self.session = None
        self.ws = None

    def set_state_manager(self, state_manager):
        self._state_manager = state_manager

    def _update_tid(self):
        if self._tid >= 9900:
            self._tid = 1
        else:
            self._tid = self._tid + 1

    async def open_session(self):
        self.session = aiohttp.ClientSession()
        try:
            self.ws = await self.session.ws_connect('ws://localhost:3456/ws')
        except Exception as conn_error:
            print("MODBUS CONNECTION: Cannot connect: ", conn_error)

    async def ws_write(self, state_dict):
        self._update_tid()
        request_serialized = _user_request_serialize(state_dict, self._state_manager, self._tid)
        try:
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            print("MODBUS_CONNECTION: Request Error: ", e)
        pending_response = asyncio.Future()
        self._pending_responses[self._tid] = pending_response
        return await pending_response

    async def ws_refresh(self):
        _automatic_request_serialize(self._state_manager)
        automatic_request = self._state_manager.live_update_states["current_request"]
        try:
            await self.ws.send_bytes(automatic_request)
        except Exception as e:
            print("MODBUS CONNECTION: Automatic Refresh Request Error: ", e)
        automatic_refresh_pending_response = asyncio.Future()
        automatic_request_tid = self._state_manager.live_update_states["current_tid"]
        self._pending_responses[automatic_request_tid] = automatic_refresh_pending_response
        await automatic_refresh_pending_response

    async def ws_read_loop(self):
        while True:
            bytes_response = await self.ws.receive()

            if isinstance(bytes_response.data, bytes):
                check_bytes = str(bytes_response.data.hex())

                if check_bytes.startswith("99"):
                    _live_update_response_deserialize(self._state_manager, bytes_response.data)
                    automatic_request_tid = self._state_manager.live_update_states["current_tid"]
                    self._pending_responses[automatic_request_tid].set_result("Done.")
                else:
                    deserialized_dict = _user_response_deserialize(bytes_response.data, self._state_manager)
                    self._pending_responses[self._tid].set_result(deserialized_dict)
