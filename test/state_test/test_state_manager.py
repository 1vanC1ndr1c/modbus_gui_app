import pytest

from modbus_gui_app.state.state_manager import StateManager


def test_state_manager():
    test_state_manager_obj = StateManager()

    assert type(test_state_manager_obj.last_ten_dicts) == dict

    # runtests.bat - v - k test_user_request_serializer.py
