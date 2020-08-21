from setuptools import setup

setup(
    name="ModbusGuiApp",
    author="Ivan Cindric",
    author_email="ivan.cindric95@example.com",
    description="ModbusGuiApplication.",
    version="1.0",
    packages=['modbus_gui_app',
              'modbus_gui_app.communication',
              'modbus_gui_app.gui',
              'modbus_gui_app.state',
              'test',
              'test.test_communication',
              'test.test_database',
              'test.test_state'
              ],
    python_requires='>=3.6',
    entry_points={'console_scripts': ['modbus_gui=modbus_gui_app.main:main']},
    install_requires=[
        'aiohttp~=3.6.2',
        'pytest~=6.0.1',
        'PySide2~=5.15.0',
        'setuptools~=49.6.0'
    ]

)
