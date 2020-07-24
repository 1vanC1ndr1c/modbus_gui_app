import sqlite3


def db_reader(db_read_queue_request, db_read_queue_response, state_manager, conn):
    while True:
        current_db_index = db_read_queue_request.get()[1]
        db_read(state_manager, db_read_queue_response, current_db_index, conn)


def db_read(state_manager, db_read_queue_response, current_db_index, conn):
    data = []
    conn = sqlite3.connect('req_and_resp.db')
    print("Reading: Connected to the DB.")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM req_and_resp "
                       "ORDER BY REQ_SENT_TIME DESC "
                       "LIMIT 10 "
                       "OFFSET " + str(current_db_index))
        data.append(cursor.fetchall())
        print("Reading successful")

        db_dict = convert_data_into_dict(data)
    except Exception as e:
        print("READING: Error!= ", e)
        db_dict = {"READ ERROR"}

    state_manager.set_db_dicts(db_dict)
    db_read_queue_response.put("READ DONE")


def convert_data_into_dict(data):
    dicts = {}
    for element in data:
        for single_dict_db in element:
            request_time_stamp = single_dict_db[0]
            tid = single_dict_db[1]
            req_type = single_dict_db[2]
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
            response_type = single_dict_db[11]
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
            dicts[request_time_stamp] = single_dict

    return dicts
