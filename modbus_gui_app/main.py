import sys

from modbus_gui_app.gui import window
from modbus_gui_app.state.state_manager import StateManager


def main():
    state_manager = StateManager()
    state_manager.start_communications_thread()
    window.run_gui(state_manager)


if __name__ == '__main__':
    sys.exit(main())
