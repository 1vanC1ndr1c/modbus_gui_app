from copy import deepcopy

import pytest

from modbus_gui_app.state import live_update
from modbus_gui_app.state.state_manager import StateManager


class MockGui:
    def __init__(self):
        self.name = "MockGui"
        self.left_side_select_operation_box = MockOpBox()


class MockOpBox:
    def __init__(self):
        self.name = "MockOpBox"
        self.current_index = 0

    def currentIndex(self):
        return self.current_index


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_set_currently_selected_automatic_request():
    st_manager = StateManager()
    st_manager.gui = MockGui()

    for i in range(1, 6):
        old_function = deepcopy(st_manager.live_update_states["currently_selected_function"])

        live_update.set_currently_selected_automatic_request(st_manager, "user")

        curr_index = st_manager.gui.left_side_select_operation_box.current_index
        st_manager.gui.left_side_select_operation_box.current_index = curr_index + 1
        live_update.set_currently_selected_automatic_request(st_manager, "user")

        new_function = st_manager.live_update_states["currently_selected_function"]

        assert old_function != new_function


async def test_process_live_update_response():
    old_dict = {1: "one", 2: "two"}
    new_dict = {1: "not one", 3: "three"}

    old_dict_org = deepcopy(old_dict)
    live_update.process_live_update_response(new_dict, old_dict)

    assert old_dict != old_dict_org
