from threading import Thread
import asyncio
import queue
import sys

from modbus_gui_app.logic.state_manager import StateManager
from modbus_connection import ModbusConnection
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.gui import window


def start_state_manager_to_modbus_link(state_manager):
    asyncio.new_event_loop().run_until_complete(
        state_manager.state_manager_to_modbus_write())


def start_app(state_manager, gui_request_queue):
    window.run_gui(state_manager, gui_request_queue)


def main():
    db_write_queue = queue.Queue()
    db_read_queue_request = queue.Queue()
    db_read_queue_response = queue.Queue()
    gui_request_queue = queue.Queue()

    state_manager = StateManager(db_read_queue_request, db_read_queue_response, db_write_queue, gui_request_queue)
    state_manager.start_communications_thread()

    start_app(state_manager, gui_request_queue)

    # database = Backend()
    # db_thread = Thread(target=database.start_db,
    #                    args=(db_write_queue, db_read_queue_request, db_read_queue_response, state_manager))
    # db_thread.start()


if __name__ == '__main__':
    sys.exit(main())
