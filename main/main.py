import asyncio
from gui import window
from communication.modbus_communication import communicate_with_modbus
from threading import Thread
import queue


def com_f(req_queue, resp_queue):
    asyncio.new_event_loop().run_until_complete(communicate_with_modbus(req_queue, resp_queue))


if __name__ == '__main__':
    request_queue = queue.Queue()
    response_queue = queue.Queue()

    # request = b'\x00\x01\x00\x00\x00\x06\x02\x01\x00"\x00\x16'  # test data
    #request_queue.put(request)


    gui_thread = Thread(target=window.init_gui, args=(request_queue, response_queue))
    com_thread = Thread(target=com_f, args=(request_queue, response_queue))

    gui_thread.start()
    com_thread.start()
