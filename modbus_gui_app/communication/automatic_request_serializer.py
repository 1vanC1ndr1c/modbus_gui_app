import re


def automatic_request_serialize(state_manager):
    function_code = state_manager.current_coil_input_reg_states["currently_selected_function"]

    if function_code == "01":
        tid = state_manager.current_coil_input_reg_states["read_coils_tid"]
        print("serializing coils")
        old_request = state_manager.current_request_and_response_dictionary["current_request_serialized"]
        print(tid, old_request)
        if old_request == b'0':
            old_request = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x01'
        old_request = re.findall('..', str(old_request.hex()))[2:]
        new_request = bytes.fromhex(str(tid) + ''.join(old_request))
        print(tid, new_request)
