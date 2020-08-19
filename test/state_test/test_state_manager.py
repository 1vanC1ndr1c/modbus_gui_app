import queue
from copy import deepcopy

from modbus_gui_app.database.db_handler import Backend
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

    def db_read(self, index):
        return "DB VALUES"

    def db_write(self, data):
        assert data == "DATA TO WRITE."


def update_history_last_ten_mock():
    pass


def write_to_db_mock():
    pass


def mock_set_currently_selected_automatic_request(*args):
    pass


def test_state_manager(monkeypatch):
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
    test_state_manager_obj._read_from_db()
    assert test_state_manager_obj._historian_db_dicts == "DB VALUES"

    test_state_manager_obj.reset_db_dict()
    assert len(test_state_manager_obj._historian_db_dicts) == 0
    assert test_state_manager_obj._historian_db_current_index == 0

    test_state_manager_obj.user_action_state = "DATA TO WRITE."
    test_state_manager_obj._write_to_db()

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
        test_state_manager_obj._process_modbus_response({1: "OnE", 2: "FOO", 9999: "NO"})

    assert True == False
    #
    # test_state_manager_obj.user_action_state = _init_user_action_state_dict()

    # runtests.bat - v - k test_user_request_serializer.py
