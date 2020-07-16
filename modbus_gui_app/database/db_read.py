import sqlite3

def db_reader(db_read_queue):
    while True:
        read_request = db_read_queue.get()
        print("READING")
        # TODO actual reading and processing
        db_read(read_request)


def db_read(request, data):
    conn = sqlite3.connect('req_and_resp.db')
    print("Writing: Connected to the DB.")
    cursor = conn.cursor()
    if request == 1:
        # get the latest entry and update the collection
        cursor.execute("SELECT * FROM req_and_resp ORDER BY TIME_STAMP DESC LIMIT 1")
        data.append(cursor.fetchone())
    elif request == 10:
        # get 10 more entries and add them to the existing ones
        print("10 more requested")
