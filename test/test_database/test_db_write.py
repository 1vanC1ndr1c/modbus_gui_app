import json
from datetime import datetime

import pytest

from modbus_gui_app.database.db_handler import Backend

executed_data = []


class MockDBConnection:
    def __init__(self):
        self.name = "MockDBConn"

    @staticmethod
    def execute(str_command, str_values):
        global executed_data
        executed_data.append(str_command)
        executed_data.append(str_values)

    @staticmethod
    def commit():
        global executed_data
        assert len(executed_data) > 0


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_db_write():
    input_dict = {
        'current_tid': 2,
        'current_unit_address': '3',
        'current_function_code': '01',
        'current_request_name': 'Read Coils.',
        'current_request_from_gui': [3, 3, 3, 1],
        'current_request_from_gui_is_valid': True,
        'current_request_from_gui_error_msg': '-',
        'current_request_serialized': b'\x00\x02\x00\x00\x00\x06\x03\x01\x00\x02\x00\x03',
        'current_request_sent_time': datetime.now(),
        'current_response_received_time': datetime.now(),
        'current_response_serialized': b'\x00\x02\x00\x00\x00\x04\x03\x01\x01\x00',
        'current_response_is_valid': True, 'current_response_err_msg': '-',
        'current_response_returned_values': '-'
    }

    test_query = "INSERT INTO REQ_AND_RESP (" \
                 "REQ_SENT_TIME, " \
                 "TID, " \
                 "REQ_TYPE, " \
                 "UNIT_ADDRESS, " \
                 "FUNCTION_CODE, " \
                 "REQ_NAME, " \
                 "REQ_FROM_GUI, " \
                 "REQ_IS_VALID, " \
                 "REQ_ERR_MSG, " \
                 "REQ_BYTE, " \
                 "RESP_REC_TIME, " \
                 "RESP_TYPE, " \
                 "RESP_BYTE, " \
                 "RESP_VALID, " \
                 "RESP_ERR_MSG, " \
                 "RESP_RET_VAL) " \
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    connection = MockDBConnection()

    database = Backend()
    database._conn = connection
    await database.db_write(input_dict)

    global executed_data
    assert test_query == executed_data[0]

    data = executed_data[1]

    assert type(data[0]) == datetime
    assert type(data[1]) == int
    assert type(data[2]) == str
    assert data[2] == "Request."
    current_unit_address = int(data[3])
    assert type(current_unit_address) == int
    f_code = int(data[4])
    assert type(f_code) == int
    assert type(data[5]) == str
    req_from_gui = json.loads(data[6])
    assert type(req_from_gui) == list
    assert type(data[7]) == bool
    if data[7] is True:
        assert data[8] == "-"
    assert type(data[9]) == bytes
    assert type(data[10]) == datetime
    assert data[11] == "Response."
    assert type(data[12]) == bytes
    assert type(data[13]) == bool
    if data[13] is True:
        assert data[14] == "-"
    assert type(data[15]) == str or type(data[15]) == bytes
