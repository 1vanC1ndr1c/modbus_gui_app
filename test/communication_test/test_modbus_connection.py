import asyncio
from collections import namedtuple
from datetime import datetime

import pytest

from modbus_gui_app.communication.modbus_connection import ModbusConnection
from modbus_gui_app.state.state_manager_data_structures import _init_live_update_states

_ResponseMock = namedtuple("_ResponseMock", ["data"])


@pytest.fixture
async def connection_factory():
    tasks = []

    def factory(mock_ws):
        test_modbus_conn = ModbusConnection()
        test_modbus_conn.ws = mock_ws

        tasks.append(asyncio.ensure_future(test_modbus_conn.ws_read_loop()))
        return test_modbus_conn

    yield factory
    for task in tasks:
        task.cancel()
        await task


class MockWs:
    def __init__(self, req_resp_dict):
        self.name = "MockWs"
        self.queue = asyncio.Queue()
        self.req_resp_dict = req_resp_dict

    async def send_bytes(self, req):
        asyncio.get_event_loop().call_soon(self.queue.put_nowait, req)

    async def receive(self):
        req = await self.queue.get()
        assert req == self.req_resp_dict["current_request_serialized"]
        return _ResponseMock(data=self.req_resp_dict["current_response_serialized"])


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_ws_read_coils(connection_factory):
    req_resp_dict = _init_live_update_states()
    req_resp_dict = req_resp_dict["current_read_coils"]
    mock_ws = MockWs(req_resp_dict)
    await connection_factory(mock_ws).ws_read_coils(1, 20, 1)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_ws_read_discrete_inputs(connection_factory):
    req_resp_dict = _init_live_update_states()
    req_resp_dict = req_resp_dict["current_read_discrete_inputs"]
    mock_ws = MockWs(req_resp_dict)
    await connection_factory(mock_ws).ws_read_discrete_inputs(1, 20, 1)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_ws_read_holding_registers(connection_factory):
    req_resp_dict = _init_live_update_states()
    req_resp_dict = req_resp_dict["current_read_holding_registers"]
    mock_ws = MockWs(req_resp_dict)
    await connection_factory(mock_ws).ws_read_holding_registers(1, 20, 1)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_ws_read_input_registers(connection_factory):
    req_resp_dict = _init_live_update_states()
    req_resp_dict = req_resp_dict["current_read_input_registers"]
    mock_ws = MockWs(req_resp_dict)
    await connection_factory(mock_ws).ws_read_input_registers(1, 20, 1)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_write_single_coil(connection_factory):
    write_coils_dict = {
        'current_tid': 1,
        'current_unit_address': '1',
        'current_function_code': '05',
        'current_request_name': 'Write Single Coil.',
        'current_request_from_gui': [1, 1, 1, 5],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00',
        'current_response_is_valid': True,
        'current_response_err_msg': '-',
        'current_response_returned_values': ['00', '01', '00', '00', '00', '06', '01', '05', '00', '00', 'ff', '00']
    }
    mock_ws = MockWs(write_coils_dict)
    await connection_factory(mock_ws).ws_write_single_coil(1, 1, 1)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_write_single_register(connection_factory):
    write_regs_dict = {
        'current_tid': 1,
        'current_unit_address': '1',
        'current_function_code': '06',
        'current_request_name': 'Write Single Register.',
        'current_request_from_gui': [1, 1, 1, 6],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x06\x00\x00\x00\x01',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x01\x00\x00\x00\x06\x01\x06\x00\x00\x00\x01',
        'current_response_is_valid': True, 'current_response_err_msg': '-',
        'current_response_returned_values': ['00', '01', '00', '00', '00', '06', '01', '06', '00', '00', '00', '01']
    }
    mock_ws = MockWs(write_regs_dict)
    await connection_factory(mock_ws).ws_write_single_register(1, 1, 1)
