from threading import Thread
import sqlite3

from modbus_gui_app.database.db_write import db_writer
from modbus_gui_app.database.db_read import db_reader


def start_db(db_write_queue, db_read_queue_request, db_read_queue_response, state_manager):
    db_init()
    db_read_thread = Thread(target=db_reader, args=(db_read_queue_request, db_read_queue_response, state_manager))
    db_read_thread.start()
    db_write_thread = Thread(target=db_writer, args=(db_write_queue,))
    db_write_thread.start()


def db_init():
    conn = sqlite3.connect('req_and_resp.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS REQ_AND_RESP(
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
    conn.close()
    print("Opened (or created) database successfully.")
