import sqlite3
from datetime import datetime


def db_init():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")

    # table: TIME_STAMP, {TYPE+TID}, PROTOCOL, LEN, UNIT_ADDRESS, FUNCTION_CODE, REQUEST

    # new_tid = "0001"
    # protocol = "0000"
    # length = "0006"
    # unit_address = "33"
    # function_code = "01"
    # modbus_request = "00100016

    # TODO implement responses into the DB

    conn.execute('''CREATE TABLE IF NOT EXISTS REQ_AND_RESP(
            TIME_STAMP      TEXT    NOT NULL,
            TYPE_AND_TID    TEXT    PRIMARY KEY     NOT NULL,
            PROTOCOL        TEXT    NOT NULL,
            LEN             TEXT    NOT NULL,
            UNIT_ADDRESS    TEXT    NOT NULL,
            F_CODE          TEXT    NOT NULL,
            MODBUS_DATA     TEXT    NOT NULL);''')

    print("'REQUESTS' Table created successfully")

    conn.close()


def db_write(db_data):
    # for el in db_data:  # organize the data
    #     print(el)
    # print("=======================")

    if db_data[0] == "REQUEST":
        apo = "\'"
        time_stamp = apo + str(datetime.now()) + apo
        tid = db_data[1]
        type_and_tid = apo + "REQ" + str(tid) + apo
        protocol = apo + str(db_data[2]) + apo
        length = apo + str(db_data[3]) + apo
        unit_address = apo + str(db_data[4]) + apo
        function_code = apo + str(db_data[5]) + apo
        modbus_request = apo + str(db_data[6]) + apo

        conn = sqlite3.connect('test.db')
        print("Opened database successfully")

        try:
            str_ins = "INSERT INTO REQ_AND_RESP (TIME_STAMP, " \
                      "TYPE_AND_TID, " \
                      "PROTOCOL, " \
                      "LEN, " \
                      "UNIT_ADDRESS, " \
                      "MODBUS_DATA) "

            # str_sep = ", "
            # conn.execute(str_ins + "VALUES (" +
            #              time_stamp + str_sep +
            #              type_and_tid + str_sep +
            #              protocol + str_sep +
            #              length + str_sep +
            #              unit_address + str_sep +
            #              function_code + str_sep +
            #              modbus_request + " )")

            # conn.execute("INSERT INTO REQ_AND_RESP (ID,NAME,AGE,ADDRESS,SALARY) \
            #       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
            #
            # conn.execute("INSERT INTO REQ_AND_RESP (ID,NAME,AGE,ADDRESS,SALARY) \
            #       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
            #
            # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

            conn.commit()
            print("Records created successfully")
            conn.close()
        except Exception as e:
            print("Error! = ", e)
