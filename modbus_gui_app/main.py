import queue
import sys

from modbus_gui_app.logic.state_manager import StateManager
from modbus_gui_app.database.db_handler import Backend
from modbus_gui_app.gui import window


def main():
    gui_request_queue = queue.Queue()
    database = Backend()
    state_manager = StateManager(gui_request_queue, database)
    database.set_st_manager(state_manager)
    state_manager.start_communications_thread()
    window.run_gui(state_manager, gui_request_queue)


if __name__ == '__main__':
    sys.exit(main())
