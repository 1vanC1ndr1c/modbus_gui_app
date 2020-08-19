Communication module
=====================

modbus_connection
""""""""""""""""""""""""
.. automodule:: modbus_gui_app.communication.modbus_connection
   :members:
   :undoc-members:
   :show-inheritance:


user_request_serializer
"""""""""""""""""""""""""""
.. automodule:: modbus_gui_app.communication.request_serializer
   :members: read_coils_serialize,
    read_discrete_inputs_serialize,
    read_holding_registers_serialize,
    read_input_registers_serialize,
    write_single_coil_serialize,
    write_single_register_serialize
   :undoc-members:
   :show-inheritance:


user_response_deserializer
"""""""""""""""""""""""""""""""""
.. automodule:: modbus_gui_app.communication.response_deserializer
   :members: response_deserialize,
    read_coils_deserialize,
    read_discrete_inputs_deserialize,
    read_holding_registers_deserialize,
    read_input_registers_deserialize,
    write_single_coil_deserialize,
    write_single_register_deserialize,
    check_for_response_errors
   :undoc-members:
   :show-inheritance:


