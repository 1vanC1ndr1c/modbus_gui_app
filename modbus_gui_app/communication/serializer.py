# tid = 0
#
# # get the dictionary and form in into bytes
# def get_serialized_request(unit_address, function_code, data, request_queue, db_write_queue):
#     # formed_request = form_request(unit_address, function_code, data, db_write_queue)
#     # request_queue.put(formed_request)
#
#
# def serialize(unit_address, function_code, data, db_write_queue):
#     # reset the tid if the maximum is reached
#     global tid
#     if tid == 9999:
#         tid = 0
#     tid = tid + 1
#     new_tid = str(tid).rjust(4, '0')  # transaction ID formed into 2 bytes
#
#     protocol = '0000'  # doesn't change
#
#     function_code = str(hex(function_code))[2:].rjust(2, '0')
#     modbus_request = function_code + ''
#
#     if function_code == '01' or function_code == '02' or function_code == '03' or function_code == '04':
#         start_add = data[0]
#         start_add = start_add - 1
#         start_add = str(hex(start_add))[2:].rjust(4, '0')
#         no_of_coils = data[1]
#         no_of_coils = str(hex(no_of_coils))[2:].rjust(4, '0')
#         modbus_request = modbus_request + start_add + no_of_coils
#
#     elif function_code == '05':
#         start_add = data[0]
#         start_add = start_add - 1
#         start_add = str(hex(start_add))[2:].rjust(4, '0')
#         state_select = data[1]
#         if state_select == 0:
#             modbus_request = modbus_request + start_add + "ff" + "00"
#         else:
#             modbus_request = modbus_request + start_add + "00" + "00"
#
#     elif function_code == '06':
#         start_add = data[0]
#         start_add = start_add - 1
#         start_add = str(hex(start_add))[2:].rjust(4, '0')
#         reg_val = data[1]
#         reg_val = str(hex(reg_val))[2:].rjust(4, '0')
#         modbus_request = modbus_request + start_add + reg_val
#
#     length = len(bytes.fromhex(modbus_request)) + 1  # defined as length of bytes after the 'length' field
#     length = str(length).rjust(4, '0')
#
#     unit_address = str(unit_address).rjust(2, '0')
#     full_request = new_tid + protocol + length + unit_address + modbus_request
#     full_request = bytes.fromhex(full_request)
#
#     db_data = ["REQUEST", new_tid, protocol, length, unit_address, function_code, modbus_request[2:]]
#     db_write_queue.put(db_data)
#
#     return full_request
#     # return b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16'    # test data
