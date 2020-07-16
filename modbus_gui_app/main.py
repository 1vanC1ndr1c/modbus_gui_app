import asyncio
import sys

from modbus_gui_app.database.db_handler import start_db
from modbus_communication import communicate_with_modbus
from modbus_gui_app.gui import window
from threading import Thread
import queue


def start_communication(req_queue, resp_queue, write_queue):
    asyncio.new_event_loop().run_until_complete(communicate_with_modbus(req_queue, resp_queue, write_queue))

def main():
    request_queue = queue.Queue()
    response_queue = queue.Queue()
    db_write_queue = queue.Queue()
    db_read_queue = queue.Queue()

    com_thread = Thread(target=start_communication, args=(request_queue, response_queue, db_write_queue))
    gui_thread = Thread(target=window.init_gui, args=(request_queue, response_queue, db_write_queue, db_read_queue))
    db_thread = Thread(target=start_db, args=(db_write_queue, db_read_queue))

    gui_thread.start()
    com_thread.start()
    #db_thread.start()

    # TEST STUFF
    # database test REQUEST
    # new_tid = "0001"
    # protocol = "0000"
    # length = "0006"
    # unit_address = "33"
    # function_code = "01"
    # modbus_request = "00100016"
    # db_data = ["REQUEST", new_tid, protocol, length, unit_address, function_code, modbus_request[2:]]
    # db_write_queue.put(db_data)
    #
    # # database test RESPONSE 1
    # # db_data = []
    # # resp1 = b'\x00\x01\x00\x00\x00\x04\x02\x01\x01\x01'
    # # db_data.append("RESPONSE")
    # # db_data.append(resp1)
    # # db_write_queue.put(db_data)
    #
    # # # database test RESPONSE 2
    # db_data = []
    # resp2 = b'\x00\x02\x00\x00\x00\x03\x03\x81\x02'
    # db_data.append("RESPONSE")
    # db_data.append(resp2)
    # # db_write(db_data)
    # db_write_queue.put(db_data)

    # request = b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16'  # test data
    # request_queue.put(request)

if __name__ == '__main__':
   sys.exit(main())
