import queue
from copy import deepcopy

import pytest

from modbus_gui_app.db_handler import Backend
from modbus_gui_app.state import live_update
from modbus_gui_app.state.state_manager import StateManager


class MockGui:
    def __init__(self):
        self.name = "MockGui"
        self.left_side_select_operation_box = MockOpBox()


class MockOpBox:
    def __init__(self):
        self.name = "MockOpBox"
        self.current_index = 1

    def currentIndex(self):
        return self.current_index


class MockDatabase:
    def __init__(self):
        self.name = "MockDB"
        self.db_closed = False

    async def db_read(self, index):
        return {1: "DB VALUES"}

    async def db_write(self, data):
        assert data[1] == "ACTION STATE"

    def db_close(self):
        self.db_closed = True

    async def db_init(self):
        return


class MockModbusConnection:
    def __init__(self):
        self.name = "MockModbusConn"
        self.tid = 1
        self.conn_close = False

    async def open_session(self):
        print("mock open")
        return

    async def ws_read_coils(self, *args):
        pass

    async def ws_read_discrete_inputs(self, *args):
        pass

    async def ws_read_holding_registers(self, *args):
        pass

    async def ws_read_input_registers(self, *args):
        pass

    async def ws_write_single_coil(self, *args):
        pass

    async def ws_write_single_register(self, *args):
        pass

    def close_connection(self):
        self.conn_close = True


def update_history_last_ten_mock():
    pass


async def write_to_db_mock():
    pass


def mock_set_currently_selected_automatic_request(*args):
    pass


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_state_manager(monkeypatch):
    test_state_manager_obj = StateManager()

    assert type(test_state_manager_obj.last_ten_dicts) == dict
    assert type(test_state_manager_obj._database) == Backend
    assert type(test_state_manager_obj.gui_request_queue) == queue.Queue
    assert type(test_state_manager_obj.user_action_state) == dict
    assert type(test_state_manager_obj._historian_db_current_index) == int
    assert type(test_state_manager_obj._historian_db_dicts) == dict
    assert type(test_state_manager_obj._live_update_states) == dict

    test_state_manager_obj.gui = MockGui()

    test_state_manager_obj._database = MockDatabase()
    await test_state_manager_obj._read_from_db()
    assert test_state_manager_obj._historian_db_dicts == {1: "DB VALUES"}

    test_state_manager_obj.reset_db_dict()
    assert len(test_state_manager_obj._historian_db_dicts) == 0
    assert test_state_manager_obj._historian_db_current_index == 0

    test_state_manager_obj.user_action_state = {1: "ACTION STATE"}

    await test_state_manager_obj._write_to_db()

    last_ten = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten"
    }
    test_state_manager_obj.last_ten_dicts = deepcopy(last_ten)
    test_state_manager_obj.user_action_state = {"current_tid": 99}
    test_state_manager_obj._update_history_last_ten()

    with monkeypatch.context() as m:
        m.setattr(live_update, "set_currently_selected_automatic_request",
                  mock_set_currently_selected_automatic_request)
        m.setattr(test_state_manager_obj, '_update_history_last_ten', update_history_last_ten_mock)
        m.setattr(test_state_manager_obj, '_write_to_db', write_to_db_mock)
        await test_state_manager_obj._process_modbus_response({1: "OnE", 2: "FOO", 9999: "NO"})

    test_state_manager_obj._modbus_connection = MockModbusConnection()

    for i in range(1, 7):
        await test_state_manager_obj.send_request_to_modbus([[66, 66, 66, i], "User Request."])
        try:
            assert test_state_manager_obj.user_action_state["current_request_from_gui"] == [66, 66, 66, i]
        except:
            assert test_state_manager_obj.user_action_state["current_request_from_gui"][1] == int("66", 16)

        await test_state_manager_obj.send_request_to_modbus([[77, 77, 77, i], "Live update."])
        current_dict = {}
        if i == 1:
            current_dict = test_state_manager_obj.live_update_states["current_read_coils"]
        elif i == 2:
            current_dict = test_state_manager_obj.live_update_states["current_read_discrete_inputs"]
        elif i == 3:
            current_dict = test_state_manager_obj.live_update_states["current_read_holding_registers"]
        elif i == 4:
            current_dict = test_state_manager_obj.live_update_states["current_read_input_registers"]

        if i < 5:
            try:
                assert current_dict["current_request_from_gui"] == [77, 77, 77, i]
            except:
                assert current_dict["current_request_from_gui"][1] == int("77", 16)

    gui_request_queue = queue.Queue()
    req_sent = "TEST REQ"

    test_state_manager_obj.gui_request_queue = gui_request_queue
    gui_request_queue.put(req_sent)

    req_recv = test_state_manager_obj._get_msg_from_gui_queue()

    assert req_sent == req_recv

    gui_request_queue.put("End.")
    await test_state_manager_obj._gui_queue_read_loop()
    assert test_state_manager_obj._database.db_closed is True
    assert test_state_manager_obj._modbus_connection.conn_close is True

    test_state_manager_obj._historian_db_dicts = {1: "DB_DICT"}

    db_ret = test_state_manager_obj.get_historian_db_dicts()

    assert db_ret == test_state_manager_obj._historian_db_dicts
