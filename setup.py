from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name="ModbusGuiApp",
    author="Ivan Cindric",
    author_email="ivan.cindric95@example.com",
    description="ModbusGuiApplication.",
    version="0.7",
    packages=['modbus_gui_app',
              'modbus_gui_app.communication',
              'modbus_gui_app.database',
              'modbus_gui_app.database',
              'modbus_gui_app.gui',
              'modbus_gui_app.state',
              'test',
              'test.test_communication',
              'test.test_database',
              'test.test_state'
              ],
    python_requires='>=3.6',
    entry_points={'group': ['modbus_gui=modbus_gui_app.main']},
    install_requires=install_requires
)
