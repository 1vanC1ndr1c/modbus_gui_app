import asyncio
import sqlite3
from datetime import datetime


async def database_f(db_write_queue, db_read_queue):
    db_init()

    async def db_write_loop():
        while True:
            data = db_write_queue.get()
            db_write(data)

    async def db_read_loop():
        while True:
            data = db_read_queue.get()
            db_read(data)

        # run in a loop
        # when there's a request, update the below mentioned collection

        # TODO write into some collection the last 10 requests/responses
        # TODO get the read request from the read queue.
        # TODO Read request is id of request/response, and the return value is it and next 10 values

    db_write_loop_future = asyncio.ensure_future(db_write_loop())
    db_read_loop_future = asyncio.ensure_future(db_read_loop())

    await asyncio.wait([db_write_loop, db_read_loop], return_when=asyncio.FIRST_COMPLETED)

    db_write_loop_future.cancel()
    db_read_loop_future.cancel()


def db_init():
    conn = sqlite3.connect('req_and_resp.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS REQ_AND_RESP(
            ID              FLOAT   PRIMARY KEY     NOT NULL,
            TIME_STAMP      TEXT    NOT NULL,
            TYPE_AND_TID    TEXT    NOT NULL    NOT NULL,
            PROTOCOL        TEXT    NOT NULL,
            LEN             TEXT    NOT NULL,
            UNIT_ADDRESS    TEXT    NOT NULL,
            F_CODE          TEXT    NOT NULL,
            MODBUS_DATA     TEXT    NOT NULL);''')
    conn.close()
    print("Opened (or created) database successfully")


def db_write(db_data):
    conn = sqlite3.connect('req_and_resp.db')
    print("Writing: Connected to the DB.")
    cursor = conn.cursor()

    if db_data[0] == "REQUEST":  # write the request into the db
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

    else:  # write the response into the db
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

    cursor.execute("SELECT 1 FROM req_and_resp WHERE TYPE_AND_TID=" + type_and_tid)

    if cursor.fetchone():  # if found, update table
        print("Key Found! Update the DB.")
        try:
            conn.execute("UPDATE req_and_resp set " +
                         "ID = " + id + str_sep +
                         "TIME_STAMP = " + time_stamp + str_sep +
                         "PROTOCOL = " + protocol + str_sep +
                         "LEN = " + length + str_sep +
                         "UNIT_ADDRESS = " + unit_address + str_sep +
                         "F_CODE = " + function_code + str_sep +
                         "MODBUS_DATA = " + modbus_info +
                         "WHERE TYPE_AND_TID = " + type_and_tid)
            conn.commit()
            print("Records updated successfully.")
            conn.close()
        except Exception as e:
            print("Error! = ", e)

    else:  # else, insert into the table
        print("Key not found. Insert the new values into the DB.")
        str_ins = "INSERT INTO REQ_AND_RESP (TIME_STAMP, " \
                  "ID, " \
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


def db_read(data):
    print("READING")
