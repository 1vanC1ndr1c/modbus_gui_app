import json
import sqlite3

from modbus_gui_app.error_logging.error_logger import init_logger


class Backend:
    """
    This class is used to instantiate a connection to the database and provides the methods needed deal with
    that connection.
    """

    def __init__(self):
        self._conn = sqlite3.connect('req_and_resp.db', check_same_thread=False)
        self._db_init()

    def _db_init(self):
        self._conn.execute('''CREATE TABLE IF NOT EXISTS REQ_AND_RESP(
                REQ_SENT_TIME   TIMESTAMP PRIMARY KEY   NOT NULL,
                TID             INT     NOT NULL,
                REQ_TYPE        TEXT    NOT NULL,
                UNIT_ADDRESS    TEXT    NOT NULL,
                FUNCTION_CODE   TEXT    NOT NULL,
                REQ_NAME        TEXT    NOT NULL,
                REQ_FROM_GUI    TEXT    NOT NULL,
                REQ_IS_VALID    TEXT    NOT NULL,
                REQ_ERR_MSG     TEXT    NOT NULL,
                REQ_BYTE        BLOB    NOT NULL,
                RESP_REC_TIME   TIMESTAMP    NOT NULL,
                RESP_TYPE       TEXT    NOT NULL,
                RESP_BYTE       BLOB    NOT NULL,
                RESP_VALID      TEXT    NOT NULL,
                RESP_ERR_MSG    TEXT    NOT NULL,
                RESP_RET_VAL    TEXT    NOT NULL);''')

    def db_read(self, current_db_index):
        """This method is used to get the information stored in the database.

        Args:
            current_db_index(int): An index used to specify the reading location in the database.

        Returns:
            dict: Return a dictionary that contains the information stored in the database on the location
                given by the 'current_db_index'.

        """
        db_data = []
        cursor = self._conn.cursor()
        logger = init_logger(__name__)

        try:
            cursor.execute("SELECT * FROM req_and_resp "
                           "ORDER BY REQ_SENT_TIME DESC "
                           "LIMIT 10 "
                           "OFFSET " + str(current_db_index))
            db_data.append(cursor.fetchall())
            db_dict = self._convert_data_into_dict(db_data)
        except:
            logger.exception("DB_READ: Database Read Error:  \n")
            db_dict = {"READ ERROR"}

        return db_dict

    def db_write(self, dictionary):
        """Method used to store the input data into the database.

        Args:
            dictionary(dict): The dictionary that contains the values to be stored into the database.

        """
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
            self._conn.execute(str_ins + "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                               (req_time_stamp, tid, req_type, unit_address, f_code,
                                req_f_code_name, req_from_gui, req_validity, req_err_msg,
                                req_byte, resp_time_stamp, resp_type, resp_byte, resp_validity,
                                resp_err_msg, resp_return_value))
            self._conn.commit()
        except:
            logger.exception("DB_WRITE: Database Writing Error:  \n")

    def db_close(self):
        """Method used to close the database connection.

        """
        self._conn.close()

    def _convert_data_into_dict(self, db_data):
        db_dicts = {}
        for element in db_data:
            for single_dict_db in element:
                request_time_stamp = single_dict_db[0]
                tid = single_dict_db[1]
                unit_address = single_dict_db[3]
                function_code = single_dict_db[4]
                request_name = single_dict_db[5]
                request_from_qui = single_dict_db[6]
                request_from_qui = json.loads(request_from_qui)
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
