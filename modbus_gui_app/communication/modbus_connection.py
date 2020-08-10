import asyncio
import re
from datetime import datetime

import aiohttp

from modbus_gui_app.communication.live_update_req_serializer import _automatic_request_serialize
from modbus_gui_app.communication.live_update_resp_deserializer import _live_update_response_deserialize
from modbus_gui_app.communication.user_request_serializer import read_coils_serialize2, \
    read_discrete_inputs_serialize, read_holding_registers_serialize, read_input_registers_serialize
from modbus_gui_app.communication.user_request_serializer import write_single_coil_serialize, \
    write_single_register_serialize
from modbus_gui_app.communication.user_response_deserializer import _user_response_deserialize
from modbus_gui_app.error_logging.error_logger import init_logger


class ModbusConnection:

    def __init__(self):
        self.user_action_dict = {
            "current_tid": 0,
            "current_unit_address": "00",
            "current_function_code": "00",
            "current_request_name": "Unknown Request.",
            "current_request_from_gui": '-',
            "current_request_from_gui_is_valid": True,
            "current_request_from_gui_error_msg": "-",
            "current_request_serialized": b'0',
            "current_request_sent_time": 0,
            "current_response_received_time": 0,
            "current_response_serialized": b'0',
            "current_response_is_valid": False,
            "current_response_err_msg": "-",
            "current_response_returned_values": "-",
        }
        self.dicts_by_tid = {}
        self.tid = 0
        self._pending_responses = {}
        self.session = None
        self.ws = None
        self.live_update_states = {}
        self.logger = init_logger(__name__)

    def _update_tid(self):
        if self.tid >= 9900:
            self.tid = 1
        else:
            self.tid = self.tid + 1

    async def open_session(self):
        self.session = aiohttp.ClientSession()
        try:
            self.ws = await self.session.ws_connect('ws://localhost:3456/ws', timeout=1000.0)
        except Exception as conn_error:
            self.logger.exception("MODBUS CONNECTION: Cannot connect:\n" + str(conn_error))

    async def ws_read_coils(self, start_addr, no_of_coils, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = read_coils_serialize2(start_addr, no_of_coils, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
            print(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Coils Request Error:\n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_read_discrete_inputs(self, start_addr, input_count, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = read_discrete_inputs_serialize(start_addr, input_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Discrete Inputs Request Error:\n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_read_holding_registers(self, start_addr, h_regs_count, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Holding Registers Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_read_input_registers(self, start_addr, in_regs_count, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = read_input_registers_serialize(start_addr, in_regs_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Input Registers Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_write_single_coil(self, start_addr, coil_state, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = write_single_coil_serialize(start_addr, coil_state, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION:  Write Single Coil Request Error:  \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_write_single_register(self, start_addr, reg_value, unit_addr):
        self._update_tid()
        request_serialized, comm_dict = write_single_register_serialize(start_addr, reg_value, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION:  Write Single Register Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        return await pending_response

    async def ws_read_loop(self):
        while True:
            bytes_response = await self.ws.receive()
            print(bytes_response)
            if bytes_response.data is None:
                breakpoint()
            if isinstance(bytes_response.data, bytes):
                check_bytes = str(bytes_response.data.hex())
                if check_bytes.startswith("99"):
                    _live_update_response_deserialize(self.live_update_states, bytes_response.data)
                    automatic_request_tid = self.live_update_states["current_tid"]
                    self._pending_responses[automatic_request_tid].set_result("Done.")
                else:
                    resp_tid = int(''.join(re.findall('..', str(bytes_response.data.hex()))[:2]))
                    req_dict = self.dicts_by_tid[resp_tid]
                    deserialized_dict = _user_response_deserialize(bytes_response.data, req_dict)
                    self._pending_responses[resp_tid].set_result(deserialized_dict)

    async def ws_refresh(self):
        _automatic_request_serialize(self.live_update_states)
        automatic_request = self.live_update_states["current_request"]
        try:
            await self.ws.send_bytes(automatic_request)
        except Exception as e:
            self.logger.exception("MODBUS CONNECTION: Automatic Refresh Request Error: \n" + str(e))
        automatic_refresh_pending_response = asyncio.Future()
        automatic_request_tid = self.live_update_states["current_tid"]
        self._pending_responses[automatic_request_tid] = automatic_refresh_pending_response
        await automatic_refresh_pending_response
