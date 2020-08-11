import asyncio
import re
from datetime import datetime

import aiohttp

from modbus_gui_app.communication.live_update_req_serializer import _automatic_request_serialize
from modbus_gui_app.communication.live_update_resp_deserializer import _live_update_response_deserialize
from modbus_gui_app.communication.user_request_serializer import read_coils_serialize, \
    read_discrete_inputs_serialize, read_holding_registers_serialize, read_input_registers_serialize
from modbus_gui_app.communication.user_request_serializer import write_single_coil_serialize, \
    write_single_register_serialize
from modbus_gui_app.communication.user_response_deserializer import user_response_deserialize
from modbus_gui_app.error_logging.error_logger import init_logger


class ModbusConnection:
    """ A class that is used for the communication between the application and modbus devices.

    Attributes:
        user_action_dict(dict): A dictionary that contains the current information being exchanged between
                                the device and user generated actions (i.e. requests and responses).

        dicts_by_tid(dict): A dictionary that contains the aforementioned user action dictionaries that get assigned
                            with a transaction id (tid) when the request is being generated. That TID is used to
                            differentiate between user actions (transaction IDs are unique).

        tid(int): A unique transaction ID that incrementally changes whenever a request is being generated. Every
                  pair of request and response is saved to a dictionary that contains that ID. When the ID reaches
                  the maximum hexadecimal value of 0xFFFF, it resets to 0x0000.

        session(aiohttp.ClientSession()): A variable that is used so that the session can be opened and close by an
                                          outside actor.

        live_update_states(dict): A dictionary that contains the current information being exchanged between the
                                  device and automatically generated requests (live update of the information).

        logger(modbus_gui_app.error_logging.error_logger): A custom logger object that writes any exceptions raised
                                                           into a file.
    """

    def __init__(self):
        self.user_action_dict = {
            "current_tid": 0,
            "current_unit_address": "00",
            "current_function_code": "00",
            "current_request_name": "Unknown Request.",
            "current_request_from_gui": '-',
            "current_request_from_gui_is_valid": True,
            "current_request_from_gui_error_msg": "-",
            "current_request_serialized": b'0',
            "current_request_sent_time": 0,
            "current_response_received_time": 0,
            "current_response_serialized": b'0',
            "current_response_is_valid": False,
            "current_response_err_msg": "-",
            "current_response_returned_values": "-",
        }
        self.dicts_by_tid = {}
        self.tid = 0
        self._pending_responses = {}
        self.session = None
        self.ws = None
        self.live_update_states = {}
        self.logger = init_logger(__name__)
        self._user_req_list = []

    def _update_tid(self):
        if self.tid >= 0xffff:
            self.tid = 0
        self.tid = self.tid + 1

    async def open_session(self):
        """  A method that opens an aiohttp.ClientSession() and logs an exception if one happens.

        Raises:
            Exception: An exception is raised if the connection cannot be established. The error is logged.
        """
        self.session = aiohttp.ClientSession()
        try:
            self.ws = await self.session.ws_connect('ws://localhost:3456/ws')
        except Exception as conn_error:
            self.logger.exception("MODBUS CONNECTION: Cannot connect:\n" + str(conn_error))

    async def ws_read_coils(self, start_addr, no_of_coils, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads coils from a specified device.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            no_of_coils(int): The specified number of coils to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            pending_response(dict): A dictionary that contains the deserialized response and the information about it.

        Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
        """
        self._update_tid()
        request_serialized, comm_dict = read_coils_serialize(start_addr, no_of_coils, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Coils Request Error:\n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_read_discrete_inputs(self, start_addr, input_count, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads discrete inputs
            from a specified device.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            input_count(int): The specified number of discrete inputs to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            pending_response(dict): A dictionary that contains the deserialized response and the information about it.

        Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
        """
        self._update_tid()
        request_serialized, comm_dict = read_discrete_inputs_serialize(start_addr, input_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Discrete Inputs Request Error:\n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_read_holding_registers(self, start_addr, h_regs_count, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads holding registers
            from a specified device.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            h_regs_count(int): The specified number of holding registers to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            pending_response(dict): A dictionary that contains the deserialized response and the information about it.

        Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
        """
        self._update_tid()
        request_serialized, comm_dict = read_holding_registers_serialize(start_addr, h_regs_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Holding Registers Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_read_input_registers(self, start_addr, in_regs_count, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads input registers
            from a specified device.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            in_regs_count(int): The specified number of holding registers to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            pending_response(dict): A dictionary that contains the deserialized response and the information about it.

        Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
        """
        self._update_tid()
        request_serialized, comm_dict = read_input_registers_serialize(start_addr, in_regs_count, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION: Read Input Registers Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_write_single_coil(self, start_addr, coil_state, unit_addr):
        """ A method that transforms the given arguments into a byte request that writes a coil value
            into a specified device.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            coil_state(int): Value to be written in a coil. It can only be 1 or 0.
            unit_addr(int): The unit address on the device.

        Returns:
            pending_response(dict): A dictionary that contains the deserialized response and the information about it.

        Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
        """
        self._update_tid()
        request_serialized, comm_dict = write_single_coil_serialize(start_addr, coil_state, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION:  Write Single Coil Request Error:  \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_write_single_register(self, start_addr, reg_value, unit_addr):
        """ A method that transforms the given arguments into a byte request that writes a coil value
              into a specified device.
          Args:
              start_addr(int): The starting address from which the coils are being read.
              reg_value(int): Value to be written in a register
              unit_addr(int): The unit address on the device.

          Returns:
              pending_response(dict): A dictionary that contains the deserialized response and the information about it.

          Raises:
            Exception: An exception is raised if the request is not sent. The error is logged.
          """
        self._update_tid()
        request_serialized, comm_dict = write_single_register_serialize(start_addr, reg_value, unit_addr, self.tid)
        self.user_action_dict.update(comm_dict)
        self.dicts_by_tid[self.tid] = self.user_action_dict
        try:
            self.user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except Exception as e:
            self.logger.exception("MODBUS_CONNECTION:  Write Single Register Request Error: \n" + str(e))
        pending_response = asyncio.Future()
        self._pending_responses[self.tid] = pending_response
        self._user_req_list.append(self.tid)
        return await pending_response

    async def ws_read_loop(self):
        """ This method continuously reads the incoming responses and processes them.
            It ignores the start of the communication and end of the communication messages (ACK, CLOSE, CLOSED...)
            and only takes into a consideration the messages that contain byte data in their body.
            Those messages are split into responses to the automatic requests and responses to a user request.
        """
        while True:
            bytes_response = await self.ws.receive()
            if isinstance(bytes_response.data, bytes):
                resp_tid = int(''.join(re.findall('..', str(bytes_response.data.hex()))[:2]), 16)
                if resp_tid not in self._user_req_list:
                    _live_update_response_deserialize(self.live_update_states, bytes_response.data)
                    self._pending_responses[resp_tid].set_result("Done.")
                else:
                    self._user_req_list.remove(resp_tid)
                    req_dict = self.dicts_by_tid[resp_tid]
                    deserialized_dict = user_response_deserialize(bytes_response.data, req_dict)
                    self._pending_responses[resp_tid].set_result(deserialized_dict)

    async def ws_refresh(self):
        """This is a generic method that is called by an outside live-update handler.
           It is used to serialize and send a request for the automatic refresh of the data being used in the program.

           Raises:
               Exception: An exception is raised if the data was not sent.
        """
        self._update_tid()
        _automatic_request_serialize(self.live_update_states, self.tid)
        automatic_request = self.live_update_states["current_request"]
        try:
            await self.ws.send_bytes(automatic_request)
        except Exception as e:
            self.logger.exception("MODBUS CONNECTION: Automatic Refresh Request Error: \n" + str(e))
        automatic_refresh_pending_response = asyncio.Future()
        self._pending_responses[self.tid] = automatic_refresh_pending_response
        await automatic_refresh_pending_response
