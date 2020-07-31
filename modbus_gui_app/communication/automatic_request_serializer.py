import re
from datetime import datetime


def automatic_request_serialize(state_manager):
    function_code = state_manager.current_coil_input_reg_states["currently_selected_function"]

    if function_code == "01":
        old_request = state_manager.current_coil_input_reg_states["current_request"]
        current_tid = state_manager.current_coil_input_reg_states["read_coils_tid"]
        valid = state_manager.current_coil_input_reg_states["current_read_coils"]["current_request_from_gui_is_valid"]
        if old_request == b'0' or valid is False:
            old_request = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14'
        old_request = re.findall('..', str(old_request.hex()))[2:]
        new_request = bytes.fromhex(str(current_tid) + ''.join(old_request))
        state_manager.current_coil_input_reg_states["current_read_coils"]["current_request_serialized"] = new_request
        state_manager.current_coil_input_reg_states["current_read_coils"]["current_request_sent_time"] = datetime.now()
        state_manager.current_coil_input_reg_states["current_request"] = new_request
        state_manager.current_coil_input_reg_states["current_tid"] = current_tid
