import sqlite3

from modbus_gui_app.database.db_read import _db_reader
from modbus_gui_app.database.db_write import _db_writer


class Backend:
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
        return _db_reader(current_db_index, self._conn)

    def db_write(self, dictionary):
        _db_writer(dictionary, self._conn)

    def db_close(self):
        self._conn.close()
