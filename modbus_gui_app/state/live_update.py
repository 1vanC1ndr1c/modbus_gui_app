import asyncio
from datetime import datetime


async def _live_update_loop(state_manager):
    while True:
        set_currently_selected_automatic_request(state_manager, "automatic")
        state_manager.connection_info_signal.emit("Automatic Request Sent.")
        current_function_code = state_manager.gui.left_side_select_operation_box.currentIndex() + 1

        req_from_gui = {"current_request_from_gui": [1, 1, 1, 1]}

        if current_function_code == 1:
            req_from_gui = state_manager.live_update_states["current_read_coils"]
        elif current_function_code == 2:
            req_from_gui = state_manager.live_update_states["current_read_discrete_inputs"]
        elif current_function_code == 3:
            req_from_gui = state_manager.live_update_states["current_read_holding_registers"]
        elif current_function_code == 4:
            req_from_gui = state_manager.live_update_states["current_read_input_registers"]
        elif current_function_code == 5:
            req_from_gui = state_manager.live_update_states["current_read_coils"]
        elif current_function_code == 6:
            req_from_gui = state_manager.live_update_states["current_read_input_registers"]

        req_from_gui = req_from_gui["current_request_from_gui"]
        await state_manager.send_request_to_modbus([req_from_gui, "Live Update."])

        state_manager.periodic_update_signal.emit(False)
        state_manager.connection_info_signal.emit("Automatic Request Received.")
        await asyncio.sleep(1)


def set_currently_selected_automatic_request(state_manager, source):
    """A method that updates the states of the currently used valid user requests.

    Args:
        state_manager: An object that contains the state that needs updating
        source: The source that triggered the update ("user" or an "automatic" update).
    """
    f_code = str(hex(state_manager.gui.left_side_select_operation_box.currentIndex() + 1))[2:].rjust(2, '0')
    state_manager.live_update_states["currently_selected_function"] = f_code

    if f_code == '01':
        req = state_manager.live_update_states["current_read_coils"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_coils_state(state_manager, source)

    elif f_code == '02':
        req = state_manager.live_update_states["current_read_discrete_inputs"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_discrete_inputs_state(state_manager, source)

    elif f_code == '03':
        req = state_manager.live_update_states["current_read_holding_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_holding_registers_state(state_manager, source)

    elif f_code == '04':
        req = state_manager.live_update_states["current_read_input_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_input_registers_state(state_manager, source)

    elif f_code == '05':
        state_manager.live_update_states["currently_selected_function"] = '01'
        req = state_manager.live_update_states["current_read_coils"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_coils_state(state_manager, "automatic")

    elif f_code == '06':
        state_manager.live_update_states["currently_selected_function"] = '04'
        req = state_manager.live_update_states["current_read_input_registers"]["current_request_serialized"]
        state_manager.live_update_states["current_request"] = req
        _update_current_input_registers_state(state_manager, "automatic")


def process_live_update_response(new_dict, old_dict):
    """Function that updated the existing dictionary with new values, if the keys of such values already exist
            in the existing dictionary.

    Args:
        new_dict: A dictionary with new values that need to be added.
        old_dict: An existing dictionary that will be updated.
    """
    old_dict["current_response_received_time"] = datetime.now()
    if new_dict != "-":
        for key in new_dict:
            if key in old_dict:
                old_dict[key] = new_dict[key]


def _update_current_coils_state(state_manager, source):
    state_manager.live_update_states["currently_selected_function"] = "01"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_coils"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        new_dict = state_manager.live_update_states["current_read_coils"]
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_coils"] = new_dict


def _update_current_discrete_inputs_state(state_manager, source):
    state_manager.live_update_states["currently_selected_function"] = "02"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_discrete_inputs"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        new_dict = state_manager.live_update_states["current_read_discrete_inputs"]
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_discrete_inputs"] = new_dict


def _update_current_holding_registers_state(state_manager, source):
    state_manager.live_update_states["currently_selected_function"] = "03"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_holding_registers"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        new_dict = state_manager.live_update_states["current_read_holding_registers"]
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_holding_registers"] = new_dict


def _update_current_input_registers_state(state_manager, source):
    state_manager.live_update_states["currently_selected_function"] = "04"
    if source == "user":
        current_state = state_manager.user_action_state
        state_manager.live_update_states["current_read_input_registers"] = current_state.copy()
        state_manager.live_update_states["current_request"] = current_state["current_request_serialized"]
    elif source == "automatic":
        new_dict = state_manager.live_update_states["current_read_input_registers"]
        new_dict["current_request_from_gui_is_valid"] = True
        state_manager.live_update_states["current_read_input_registers"] = new_dict
