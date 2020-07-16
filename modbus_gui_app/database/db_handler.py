import sqlite3
from threading import Thread

from modbus_gui_app.database.db_read import db_reader
from modbus_gui_app.database.db_write import db_writer


def start_db(db_write_queue, db_read_queue):
    db_init()
    db_read_thread = Thread(target=db_reader, args=(db_read_queue,))
    db_read_thread.start()
    db_write_thread = Thread(target=db_writer, args=(db_write_queue, db_read_queue))
    db_write_thread.start()


def db_init():
    conn = sqlite3.connect('req_and_resp.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS REQ_AND_RESP(
            INDEX_AND_TYPE  FLOAT   NOT NULL,
            TIME_STAMP      TIMESTAMP PRIMARY KEY   NOT NULL,
            TYPE_AND_TID    TEXT    NOT NULL    NOT NULL,
            PROTOCOL        TEXT    NOT NULL,
            LEN             TEXT    NOT NULL,
            UNIT_ADDRESS    TEXT    NOT NULL,
            F_CODE          TEXT    NOT NULL,
            MODBUS_DATA     TEXT    NOT NULL);''')
    conn.close()
    print("Opened (or created) database successfully")
