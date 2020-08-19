import asyncio
import logging
import sys
from threading import Thread

from modbus_gui_app.gui import window
from modbus_gui_app.state.state_manager import StateManager


def main():
    up_line = "===================================================================================================\n"
    f = up_line + '%(asctime)s \n %(message)s'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format=f)

    state_manager = StateManager()
    communications_thread = Thread(
        daemon=True,
        target=lambda: asyncio.new_event_loop().run_until_complete(state_manager.start_readers_and_writers())
    )
    communications_thread.start()

    window.run_gui(state_manager)


if __name__ == '__main__':
    sys.exit(main())
