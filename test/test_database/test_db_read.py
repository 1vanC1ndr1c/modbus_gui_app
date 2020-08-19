from datetime import datetime

import pytest

from modbus_gui_app.database.db_handler import Backend


class MockDBConnection:
    def __init__(self):
        self.name = "MockDBConn"

    @staticmethod
    def cursor():
        return MockCursor()


class MockCursor:
    def __init__(self):
        self.name = "MockCursor"
        self.mock_data = []

    def execute(self, str_req):
        self.mock_data = [
            (
                '2020-08-14 09:40:31.007431', 20, 'Request.', '3', '05',
                'Write Single Coil.', '[4, 0, 3, 5]', '1', '-',
                b'\x00\x14\x00\x00\x00\x06\x03\x05\x00\x03\x00\x00',
                '2020-08-14 09:40:31.008391', 'Response.',
                b'\x00\x14\x00\x00\x00\x06\x03\x05\x00\x03\x00\x00', '1', '-',
                "['00', '14', '00', '00', '00', '06', '03', '05', '00', '03', '00', '00']"
            ),
            (
                '2020-08-14 09:40:27.671248', 15, 'Request.', '3', '05',
                'Write Single Coil.', '[4, 1, 3, 5]', '1', '-',
                b'\x00\x0f\x00\x00\x00\x06\x03\x05\x00\x03\xff\x00',
                '2020-08-14 09:40:27.672215', 'Response.',
                b'\x00\x0f\x00\x00\x00\x06\x03\x05\x00\x03\xff\x00', '1', '-',
                "['00', '0f', '00', '00', '00', '06', '03', '05', '00', '03', 'ff', '00']"
            ),
            (
                '2020-08-14 09:40:22.647687', 9, 'Request.', '4', '05',
                'Write Single Coil.', '[4, 1, 4, 5]', '1', '-',
                b'\x00\t\x00\x00\x00\x06\x04\x05\x00\x03\xff\x00',
                '2020-08-14 09:40:22.648684', 'Response.',
                b'\x00\t\x00\x00\x00\x06\x04\x05\x00\x03\xff\x00', '1', '-',
                "['00', '09', '00', '00', '00', '06', '04', '05', '00', '03', 'ff', '00']"
            ),
            (
                '2020-08-14 09:40:16.439364', 2, 'Request.', '3', '01',
                'Read Coils.', '[3, 3, 3, 1]', '1', '-',
                b'\x00\x02\x00\x00\x00\x06\x03\x01\x00\x02\x00\x03',
                '2020-08-14 09:40:16.440331', 'Response.',
                b'\x00\x02\x00\x00\x00\x04\x03\x01\x01\x01', '1', '-', "['0x3']"
            ),
            (
                '2020-08-14 09:34:14.703967', 24, 'Request.', '3', '06',
                'Write Single Register.', '[4, 3, 3, 6]', '1', '-',
                b'\x00\x18\x00\x00\x00\x06\x03\x06\x00\x03\x00\x03', '2020-08-14 09:34:14.704964',
                'Response.', b'\x00\x18\x00\x00\x00\x06\x03\x06\x00\x03\x00\x03', '1', '-',
                "b'\\x00\\x18\\x00\\x00\\x00\\x06\\x03\\x06\\x00\\x03\\x00\\x03'"),
            (
                '2020-08-14 09:34:10.095085', 19, 'Request.', '3', '04',
                'Read Input Registers.', '[3, 3, 3, 4]', '1', '-',
                b'\x00\x13\x00\x00\x00\x06\x03\x04\x00\x02\x00\x03',
                '2020-08-14 09:34:10.097079', 'Response.',
                b'\x00\x13\x00\x00\x00\t\x03\x04\x06\x00\x03\x00\x00\x00\x00', '1', '-', "[['0x3', '0003']]"
            ),
            (
                '2020-08-14 09:34:06.087590', 14, 'Request.', '3', '06',
                'Write Single Register.', '[3, 3, 3, 6]', '1', '-',
                b'\x00\x0e\x00\x00\x00\x06\x03\x06\x00\x02\x00\x03',
                '2020-08-14 09:34:06.088556', 'Response.',
                b'\x00\x0e\x00\x00\x00\x06\x03\x06\x00\x02\x00\x03', '1', '-',
                "b'\\x00\\x0e\\x00\\x00\\x00\\x06\\x03\\x06\\x00\\x02\\x00\\x03'"),
            (
                '2020-08-14 09:34:01.607386', 8, 'Request.', '3', '01',
                'Read Coils.', '[3, 3, 3, 1]', '1', '-',
                b'\x00\x08\x00\x00\x00\x06\x03\x01\x00\x02\x00\x03',
                '2020-08-14 09:34:01.608383', 'Response.',
                b'\x00\x08\x00\x00\x00\x04\x03\x01\x01\x01', '1', '-', "['0x3']"
            ),
            (
                '2020-08-14 09:33:57.016498', 3, 'Request.', '3', '05',
                'Write Single Coil.', '[3, 1, 3, 5]', '1', '-',
                b'\x00\x03\x00\x00\x00\x06\x03\x05\x00\x02\xff\x00',
                '2020-08-14 09:33:57.017465', 'Response.',
                b'\x00\x03\x00\x00\x00\x06\x03\x05\x00\x02\xff\x00', '1', '-',
                "b'\\x00\\x03\\x00\\x00\\x00\\x06\\x03\\x05\\x00\\x02\\xff\\x00'"
            ),
            (
                '2020-08-14 09:28:20.535090', 4, 'Request.', '3', '01',
                'Read Coils.', '[3, 3, 3, 1]', '1', '-',
                b'\x00\x04\x00\x00\x00\x06\x03\x01\x00\x02\x00\x03',
                '2020-08-14 09:28:20.536056', 'Response.',
                b'\x00\x04\x00\x00\x00\x04\x03\x01\x01\x00', '1', '-', '-'
            )
        ]

    def fetchall(self):
        return self.mock_data


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_db_reader():
    current_db_index = 30
    connection = MockDBConnection()

    database = Backend()
    database._conn = connection

    db_dicts = (await database.db_read(current_db_index))

    for time_stamp_dict_key in db_dicts:
        datetime.strptime(time_stamp_dict_key, "%Y-%m-%d %H:%M:%S.%f")
        current_dict = db_dicts[time_stamp_dict_key]

        assert type(current_dict["current_tid"]) == int

        unit_addr = int(current_dict["current_unit_address"])

        f_code = int(current_dict["current_function_code"])

        assert type(current_dict["current_request_name"]) == str

        assert type(current_dict["current_request_from_gui"]) == list

        assert type(current_dict["current_request_from_gui_is_valid"]) == bool

        assert type(current_dict["current_request_from_gui_error_msg"]) == str

        if current_dict["current_request_from_gui_is_valid"] is True:
            assert current_dict["current_request_from_gui_error_msg"] == "-"

        assert type(current_dict["current_request_serialized"]) == bytes

        datetime.strptime(current_dict["current_request_sent_time"], "%Y-%m-%d %H:%M:%S.%f")
        datetime.strptime(current_dict["current_response_received_time"], "%Y-%m-%d %H:%M:%S.%f")

        assert type(current_dict["current_response_serialized"]) == bytes

        assert type(current_dict["current_response_is_valid"]) == bool

        assert type(current_dict["current_response_err_msg"]) == str

        if current_dict["current_response_is_valid"] is True:
            assert current_dict["current_response_err_msg"] == "-"

        assert type(current_dict["current_response_returned_values"]) == bytes \
               or type(current_dict["current_response_returned_values"]) == str
