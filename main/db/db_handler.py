import sqlite3


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

    conn.execute('''CREATE TABLE IF NOT EXISTS REQUESTS(
            TIME_STAMP      TEXT    NOT NULL,
            TYPE_AND_TID    INT     PRIMARY KEY     NOT NULL,
            TYPE            TEXT    NOT NULL,
            PROTOCOL        TEXT    NOT NULL,
            LEN             TEXT    NOT NULL,
            UNIT_ADDRESS    TEXT    NOT NULL,
            MODBUS_DATA     TEXT    NOT NULL);''')

    print("'REQUESTS' Table created successfully")

    conn.close()


def db_write(db_data):
    for el in db_data:
        print(el)

    # TODO first select, then based on the result, do INSERT or UPDATE
    # conn = sqlite3.connect('test.db')
    # print("Opened database successfully")
    #
    # try:
    #     conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #           VALUES (1, 'Paul', 32, 'California', 20000.00 )")
    #
    #     conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #           VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
    #
    #     conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #           VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
    #
    #     conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
    #
    #     conn.commit()
    #     print("Records created successfully")
    #     conn.close()
    # except:
    #     print("Error!")
