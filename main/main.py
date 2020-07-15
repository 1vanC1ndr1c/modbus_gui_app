import asyncio

from db_handler import db_init, db_write
from gui import window
from communication.modbus_communication import communicate_with_modbus
from threading import Thread
import queue

from request_processing import send_request, form_request


def com_f(req_queue, resp_queue):
    asyncio.new_event_loop().run_until_complete(communicate_with_modbus(req_queue, resp_queue))


if __name__ == '__main__':
    # request_queue = queue.Queue()
    # response_queue = queue.Queue()
    #
    # gui_thread = Thread(target=window.init_gui, args=(request_queue, response_queue))
    #
    # com_thread = Thread(target=com_f, args=(request_queue, response_queue))
    #
    # gui_thread.start()
    # com_thread.start()

    # request = b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16'  # test data
    # request_queue.put(request)


    db_init()
    # db test REQUEST
    new_tid = "0001"
    protocol = "0000"
    length = "0006"
    unit_address = "33"
    function_code = "01"
    modbus_request = "00100016"
    db_data = []
    db_data.append("REQUEST")
    db_data.append(new_tid)
    db_data.append(protocol)
    db_data.append(length)
    db_data.append(unit_address)
    db_data.append(function_code)
    db_data.append(modbus_request[2:])
    db_write(db_data)
    #
    # # db test RESPONSE 1
    # db_data = []
    # resp1 = b'\x00\x01\x00\x00\x00\x04\x02\x01\x01\x01'
    # db_data.append("RESPONSE")
    # db_data.append(resp1)
    # db_write(db_data)
    # #
    # # db test RESPONSE 2
    # db_data = []
    # resp1 = "ERROR: Illegal data address"
    # db_data.append("RESPONSE")
    # db_data.append(resp1)
    # db_write(db_data)

    # db_init()
