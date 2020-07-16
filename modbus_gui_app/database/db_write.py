import sqlite3
from datetime import datetime


def db_writer(db_write_queue, db_read_queue):
    while True:
        data = db_write_queue.get()
        db_write(data)


def db_write(db_data):
    conn = sqlite3.connect('req_and_resp.db')
    print("Writing: Connected to the DB.")
    cursor = conn.cursor()

    if db_data[0] == "REQUEST":  # write the request into the database
        str_sep = ", "
        apostrophe = "\'"
        id = str(db_data[1]) + ".1"
        time_stamp = apostrophe + str(datetime.now()) + apostrophe
        type_and_tid = apostrophe + "REQ" + str(db_data[1]) + apostrophe
        protocol = apostrophe + str(db_data[2]) + apostrophe
        length = apostrophe + str(db_data[3]) + apostrophe
        unit_address = apostrophe + str(db_data[4]) + apostrophe
        function_code = apostrophe + str(db_data[5]) + apostrophe
        modbus_info = apostrophe
        for i in range(6, len(db_data)):
            modbus_info = modbus_info + db_data[i]
        modbus_info = modbus_info + apostrophe
        # check if the entry already exists

    else:  # write the response into the database
        str_sep = ", "
        apostrophe = "\'"
        time_stamp = apostrophe + str(datetime.now()) + apostrophe
        response = str(db_data[1]).replace("x", "").replace("\'", "").split("\\")[1:]
        tid = response[0] + response[1]
        id = str(tid) + ".2"
        type_and_tid = apostrophe + "RESP" + tid + apostrophe
        protocol = apostrophe + response[2] + response[3] + apostrophe
        length = apostrophe + response[4] + response[5] + apostrophe
        unit_address = apostrophe + response[6] + apostrophe
        function_code = apostrophe + response[7] + apostrophe
        modbus_info = apostrophe
        for i in range(8, len(response)):
            modbus_info = modbus_info + response[i]
        modbus_info = modbus_info + apostrophe

        str_ins = "INSERT INTO REQ_AND_RESP (TIME_STAMP, " \
                  "INDEX_AND_TYPE, " \
                  "TYPE_AND_TID, " \
                  "PROTOCOL, " \
                  "LEN, " \
                  "UNIT_ADDRESS, " \
                  "F_CODE, " \
                  "MODBUS_DATA) "
        try:
            conn.execute(str_ins + "VALUES (" +
                         time_stamp + str_sep +
                         id + str_sep +
                         type_and_tid + str_sep +
                         protocol + str_sep +
                         length + str_sep +
                         unit_address + str_sep +
                         function_code + str_sep +
                         modbus_info + " )")

            conn.commit()
            print("Records created successfully.")
            conn.close()
        except Exception as e:
            print("Error! = ", e)