import json

from modbus_gui_app.error_logging.error_logger import init_logger


def _db_writer(dictionary, conn):
    logger = init_logger(__name__)

    req_time_stamp = dictionary["current_request_sent_time"]
    tid = dictionary["current_tid"]
    req_type = "Request."
    unit_address = dictionary["current_unit_address"]
    f_code = dictionary["current_function_code"]
    req_f_code_name = dictionary["current_request_name"]
    req_from_gui = dictionary["current_request_from_gui"]
    req_from_gui = json.dumps(req_from_gui)
    req_validity = dictionary["current_request_from_gui_is_valid"]
    req_err_msg = dictionary["current_request_from_gui_error_msg"]
    req_byte = dictionary["current_request_serialized"]
    resp_time_stamp = dictionary["current_response_received_time"]
    resp_type = "Response."
    resp_byte = dictionary["current_response_serialized"]
    resp_validity = dictionary["current_response_is_valid"]
    resp_err_msg = dictionary["current_response_err_msg"]
    resp_return_value = str(dictionary["current_response_returned_values"])

    str_ins = "INSERT INTO REQ_AND_RESP (" \
              "REQ_SENT_TIME, " \
              "TID, " \
              "REQ_TYPE, " \
              "UNIT_ADDRESS, " \
              "FUNCTION_CODE, " \
              "REQ_NAME, " \
              "REQ_FROM_GUI, " \
              "REQ_IS_VALID, " \
              "REQ_ERR_MSG, " \
              "REQ_BYTE, " \
              "RESP_REC_TIME, " \
              "RESP_TYPE, " \
              "RESP_BYTE, " \
              "RESP_VALID, " \
              "RESP_ERR_MSG, " \
              "RESP_RET_VAL) "
    try:
        conn.execute(str_ins + "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (req_time_stamp, tid, req_type, unit_address, f_code,
                      req_f_code_name, req_from_gui, req_validity, req_err_msg,
                      req_byte, resp_time_stamp, resp_type, resp_byte, resp_validity,
                      resp_err_msg, resp_return_value))
        conn.commit()
    except Exception as e:
        logger.exception("DB_WRITE: Database Writing Error:  \n" + str(e))
