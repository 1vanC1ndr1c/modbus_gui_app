from threading import Thread
import asyncio
import queue
import sys

from modbus_gui_app.logic.state_manager import StateManager
from modbus_connection import ModbusConnection
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.gui.window import start_app


def start_communication(req_queue, resp_queue, st_mngr, modbus_communicator):
    asyncio.new_event_loop().run_until_complete(
        modbus_communicator.communicate_with_modbus(req_queue, resp_queue, st_mngr))


def start_state_manager_to_modbus_link(state_manager):
    asyncio.new_event_loop().run_until_complete(
        state_manager.state_manager_to_modbus_write())


def main():
    modbus_request_queue = queue.Queue()
    modbus_response_queue = queue.Queue()
    db_write_queue = queue.Queue()
    db_read_queue_request = queue.Queue()
    db_read_queue_response = queue.Queue()
    gui_request_queue = queue.Queue()

    state_manager = StateManager(db_read_queue_request, db_read_queue_response, db_write_queue, gui_request_queue)

    # state_manager_thread = Thread(target=start_state_manager_to_modbus_link, args=(state_manager,))
    # state_manager_thread.start()
    state_manager.start_communications_thread()

    # database = Backend()
    # db_thread = Thread(target=database.start_db,
    #                    args=(db_write_queue, db_read_queue_request, db_read_queue_response, state_manager))
    # db_thread.start()

    gui_thread = Thread(target=start_app, args=(state_manager, gui_request_queue))
    gui_thread.start()


if __name__ == '__main__':
    sys.exit(main())
