import sys

from modbus_gui_app.gui import window
from modbus_gui_app.state.state_manager import StateManager
import logging


def main():
    up_line = "===================================================================================================\n"
    f = up_line + '%(asctime)s \n %(message)s'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format=f)

    state_manager = StateManager()
    state_manager.start_communications_thread()
    window.run_gui(state_manager)


if __name__ == '__main__':
    sys.exit(main())
