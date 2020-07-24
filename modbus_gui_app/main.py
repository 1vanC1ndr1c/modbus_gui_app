from threading import Thread
import asyncio
import queue
import sys

from modbus_gui_app.logic.state_manager import StateManager
from modbus_communication import ModbusCommunication
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.gui.window import start_app


def start_communication(req_queue, resp_queue, st_mngr, modbus_communicator):
    asyncio.new_event_loop().run_until_complete(
        modbus_communicator.communicate_with_modbus(req_queue, resp_queue, st_mngr))


def main():
    modbus_request_queue = queue.Queue()
    modbus_response_queue = queue.Queue()
    db_write_queue = queue.Queue()
    db_read_queue_request = queue.Queue()
    db_read_queue_response = queue.Queue()

    state_manager = StateManager(modbus_request_queue, modbus_response_queue,
                                 db_read_queue_request, db_read_queue_response,
                                 db_write_queue)
    modbus_communicator = ModbusCommunication()

    database = Backend()

    com_thread = Thread(target=start_communication,
                        args=(modbus_request_queue, modbus_response_queue, state_manager, modbus_communicator))
    com_thread.start()

    db_thread = Thread(target=database.start_db,
                       args=(db_write_queue, db_read_queue_request, db_read_queue_response, state_manager))
    db_thread.start()

    gui_thread = Thread(target=start_app, args=(state_manager,))
    gui_thread.start()


if __name__ == '__main__':
    sys.exit(main())
