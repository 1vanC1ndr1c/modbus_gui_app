def _db_reader(state_manager, current_db_index, conn):
    db_data = []
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM req_and_resp "
                       "ORDER BY REQ_SENT_TIME DESC "
                       "LIMIT 10 "
                       "OFFSET " + str(current_db_index))
        db_data.append(cursor.fetchall())
        db_dict = _convert_data_into_dict(db_data)
    except Exception as e:
        print("BR_READ: Database Read Error: ", e)
        db_dict = {"READ ERROR"}

    state_manager._historian_db_dicts = db_dict


def _convert_data_into_dict(db_data):
    db_dicts = {}
    for element in db_data:
        for single_dict_db in element:
            request_time_stamp = single_dict_db[0]
            tid = single_dict_db[1]
            unit_address = single_dict_db[3]
            function_code = single_dict_db[4]
            request_name = single_dict_db[5]
            request_from_qui = single_dict_db[6]
            request_is_valid = single_dict_db[7]
            if request_is_valid == "1":
                request_is_valid = True
            else:
                request_is_valid = False
            request_error_msg = single_dict_db[8]
            request_byte = single_dict_db[9]
            response_time_stamp = single_dict_db[10]
            response_byte = single_dict_db[12]
            response_is_valid = single_dict_db[13]
            if response_is_valid == "1":
                response_is_valid = True
            else:
                response_is_valid = False
            response_error_msg = single_dict_db[14]
            response_return_value = single_dict_db[15]

            single_dict = {
                "current_tid": tid,
                "current_unit_address": unit_address,
                "current_function_code": function_code,
                "current_request_name": request_name,
                "current_request_from_gui": request_from_qui,
                "current_request_from_gui_is_valid": request_is_valid,
                "current_request_from_gui_error_msg": request_error_msg,
                "current_request_serialized": request_byte,
                "current_request_sent_time": request_time_stamp,
                "current_response_received_time": response_time_stamp,
                "current_response_serialized": response_byte,
                "current_response_is_valid": response_is_valid,
                "current_response_err_msg": response_error_msg,
                "current_response_returned_values": response_return_value,
            }
            db_dicts[request_time_stamp] = single_dict

    return db_dicts
