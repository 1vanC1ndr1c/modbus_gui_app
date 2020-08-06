import asyncio


async def _live_update_loop(state_manager):
    while True:
        _set_currently_selected_automatic_request(state_manager, "automatic")
        state_manager.connection_info_signal.emit("Automatic Request Sent.")
        await state_manager.modbus_connection.ws_refresh()
        state_manager.periodic_update_signal.emit(False)
        state_manager.connection_info_signal.emit("Automatic Request Received.")
        await asyncio.sleep(1)


def _set_currently_selected_automatic_request(state_manager, source):
    current_function_code = state_manager.gui.left_side_select_operation_box.currentIndex() + 1

    if current_function_code == 1:
        current_function_code = str(hex(current_function_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = current_function_code
        req = state_manager.live_update_states["current_read_coils"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_coils_state(state_manager, source)

    elif current_function_code == 2:
        current_function_code = str(hex(current_function_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = current_function_code
        req = state_manager.live_update_states["current_read_discrete_inputs"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_discrete_inputs_state(state_manager, source)

    elif current_function_code == 3:
        current_function_code = str(hex(current_function_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = current_function_code
        r = state_manager.live_update_states["current_read_holding_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = r
        _update_current_holding_registers_state(state_manager, source)

    elif current_function_code == 4:
        current_function_code = str(hex(current_function_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = current_function_code
        r = state_manager.live_update_states["current_read_input_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = r
        _update_current_input_registers_state(state_manager, source)

    elif current_function_code == 5:
        f_code = 1
        f_code = str(hex(f_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = f_code
        req = state_manager.live_update_states["current_read_coils"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_coils_state(state_manager, "automatic")

    elif current_function_code == 6:
        f_code = 4
        f_code = str(hex(f_code))[2:].rjust(2, '0')
        state_manager.live_update_states["currently_selected_function"] = f_code
        req = state_manager.live_update_states["current_read_input_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_input_registers_state(state_manager, "automatic")


def _update_current_coils_state(state_manager, source):
    state_manager.live_update_states["current_tid"] = 9901
    state_manager.live_update_states["currently_selected_function"] = "01"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_coils"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        current_tid = state_manager.live_update_states["read_coils_tid"]
        new_dict = state_manager.live_update_states["current_read_coils"]
        new_dict["current_tid"] = current_tid
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_coils"] = new_dict


def _update_current_discrete_inputs_state(state_manager, source):
    state_manager.live_update_states["current_tid"] = 9902
    state_manager.live_update_states["currently_selected_function"] = "02"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_discrete_inputs"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        current_tid = state_manager.live_update_states["read_discrete_inputs_tid"]
        new_dict = state_manager.live_update_states["current_read_discrete_inputs"]
        new_dict["current_tid"] = current_tid
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_discrete_inputs"] = new_dict


def _update_current_holding_registers_state(state_manager, source):
    state_manager.live_update_states["current_tid"] = 9903
    state_manager.live_update_states["currently_selected_function"] = "03"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_holding_registers"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        current_tid = state_manager.live_update_states["read_holding_registers_tid"]
        new_dict = state_manager.live_update_states["current_read_holding_registers"]
        new_dict["current_tid"] = current_tid
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_holding_registers"] = new_dict


def _update_current_input_registers_state(state_manager, source):
    state_manager.live_update_states["current_tid"] = 9904
    state_manager.live_update_states["currently_selected_function"] = "04"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_input_registers"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        current_tid = state_manager.live_update_states["read_input_registers_tid"]
        new_dict = state_manager.live_update_states["current_read_input_registers"]
        new_dict["current_tid"] = current_tid
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_input_registers"] = new_dict
