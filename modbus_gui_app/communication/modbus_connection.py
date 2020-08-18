import asyncio
import re
from datetime import datetime

import aiohttp

from modbus_gui_app.communication.user_request_serializer import read_coils_serialize, \
    read_discrete_inputs_serialize, read_holding_registers_serialize, read_input_registers_serialize
from modbus_gui_app.communication.user_request_serializer import write_single_coil_serialize, \
    write_single_register_serialize
from modbus_gui_app.communication.user_response_deserializer import user_response_deserialize
from modbus_gui_app.error_logging.error_logger import init_logger


class ModbusConnection:
    """ A class that is used for the communication between the application and modbus devices.

    Attributes:
        _user_action_dict(dict): A dictionary that contains the current information being exchanged between
                                the device and user generated actions (i.e. requests and responses).

        _dicts_by_tid(dict): A dictionary that contains the aforementioned user action dictionaries that get assigned
                            with a transaction id (tid) when the request is being generated. That TID is used to
                            differentiate between user actions (transaction IDs are unique).

        _tid(int): A unique transaction ID that incrementally changes whenever a request is being generated. Every
                  pair of request and response is saved to a dictionary that contains that ID. When the ID reaches
                  the maximum hexadecimal value of 0xFFFF, it resets to 0x0000.

        session(aiohttp.ClientSession()): A variable that is used so that the session can be opened and close by an
                                          outside actor.

        logger(modbus_gui_app.error_logging.error_logger): A custom logger object that writes any exceptions raised
                                                           into a file.
    """

    def __init__(self):
        self._user_action_dict = {
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
        self._dicts_by_tid = {}
        self._tid = 0
        self._pending_responses = {}
        self.session = None
        self.ws = None
        self.logger = init_logger(__name__)
        self.ws_read_loop_future = None

    @property
    def dicts_by_tid(self):
        return self._dicts_by_tid

    @property
    def tid(self):
        return self._tid

    def _update_and_get_tid(self):
        if self._tid >= 0xffff:
            self._tid = 0
        self._tid = self._tid + 1
        return self._tid

    async def open_session(self):
        """  Connects to a websocket. Logs an error if one occurs.

        """
        self.session = aiohttp.ClientSession()
        try:
            self.ws = await self.session.ws_connect('ws://localhost:3456/ws')
        except:
            self.logger.exception("MODBUS CONNECTION: Cannot connect:\n")

        self.ws_read_loop_future = asyncio.ensure_future(self._ws_read_loop())

    def close_connection(self):
        try:
            self.ws_read_loop_future.cancel()
        except asyncio.CancelledError:
            pass

    async def ws_read_coils(self, start_addr, no_of_coils, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads coils from a specified device.
            Logs an error if one occurs.
        Args:
            start_addr(int): The starting address from which the coils are being read.
            no_of_coils(int): The specified number of coils to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            dict: A dictionary that contains the deserialized response and the information about it.

        """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = read_coils_serialize(start_addr, no_of_coils, unit_addr, newest_tid)

        response = await self._ws_send_request("Read Coils", request_serialized, comm_dict, newest_tid)
        return response

    async def ws_read_discrete_inputs(self, start_addr, input_count, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads discrete inputs
            from a specified device. Logs an error if one occurs.

        Args:
            start_addr(int): The starting address from which the coils are being read.
            input_count(int): The specified number of discrete inputs to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            dict: A dictionary that contains the deserialized response and the information about it.

        """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = read_discrete_inputs_serialize(start_addr, input_count, unit_addr, newest_tid)

        response = await self._ws_send_request("Read Discrete Inputs", request_serialized, comm_dict, newest_tid)
        return response

    async def ws_read_holding_registers(self, start_addr, h_regs_count, u_addr):
        """ A method that transforms the given arguments into a byte request that reads holding registers
            from a specified device. Logs an error if one occurs.

        Args:
            start_addr(int): The starting address from which the coils are being read.
            h_regs_count(int): The specified number of holding registers to be read.
            u_addr(int): The unit address on the device.

        Returns:
            dict: A dictionary that contains the deserialized response and the information about it.

        """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = read_holding_registers_serialize(start_addr, h_regs_count, u_addr, newest_tid)

        response = await self._ws_send_request("Read Holding Registers", request_serialized, comm_dict, newest_tid)
        return response

    async def ws_read_input_registers(self, start_addr, in_regs_count, unit_addr):
        """ A method that transforms the given arguments into a byte request that reads input registers
            from a specified device. Logs an error if one occurs.

        Args:
            start_addr(int): The starting address from which the coils are being read.
            in_regs_count(int): The specified number of holding registers to be read.
            unit_addr(int): The unit address on the device.

        Returns:
            dict: A dictionary that contains the deserialized response and the information about it.

        """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = read_input_registers_serialize(start_addr, in_regs_count, unit_addr, newest_tid)

        response = await self._ws_send_request("Read Input Registers", request_serialized, comm_dict, newest_tid)
        return response

    async def ws_write_single_coil(self, start_addr, coil_state, unit_addr):
        """ A method that transforms the given arguments into a byte request that writes a coil value
            into a specified device. Logs an error if one occurs.

        Args:
            start_addr(int): The starting address from which the coils are being read.
            coil_state(int): Value to be written in a coil. It can only be 1 or 0.
            unit_addr(int): The unit address on the device.

        Returns:
            dict: A dictionary that contains the deserialized response and the information about it.

        """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = write_single_coil_serialize(start_addr, coil_state, unit_addr, newest_tid)

        response = await self._ws_send_request("Write Single Coil", request_serialized, comm_dict, newest_tid)
        return response

    async def ws_write_single_register(self, start_addr, reg_value, unit_addr):
        """ A method that transforms the given arguments into a byte request that writes a coil value
              into a specified device. Logs an error if one occurs.

          Args:
              start_addr(int): The starting address from which the coils are being read.
              reg_value(int): Value to be written in a register
              unit_addr(int): The unit address on the device.

          Returns:
              dict: A dictionary that contains the deserialized response and the information about it.

          """
        newest_tid = self._update_and_get_tid()
        request_serialized, comm_dict = write_single_register_serialize(start_addr, reg_value, unit_addr, newest_tid)

        response = await self._ws_send_request("Write Single Register", request_serialized, comm_dict, newest_tid)
        return response

    async def _ws_send_request(self, req_name, request_serialized, comm_dict, newest_tid):

        self._user_action_dict.update(comm_dict)
        self._dicts_by_tid[newest_tid] = self._user_action_dict
        try:
            self._user_action_dict["current_request_sent_time"] = datetime.now()
            await self.ws.send_bytes(request_serialized)
        except:
            self.logger.exception("MODBUS_CONNECTION: " + req_name + " Request Error:\n")
        pending_response = asyncio.Future()
        self._pending_responses[newest_tid] = pending_response
        return await pending_response

    async def _ws_read_loop(self):
        """ This method continuously reads the incoming responses and processes them.
            It ignores the start of the communication and end of the communication messages (ACK, CLOSE, CLOSED...)
            and only takes into a consideration the messages that contain byte data in their body.

        """
        while True:
            try:
                bytes_response = await self.ws.receive()
            except asyncio.CancelledError:
                return
            if isinstance(bytes_response.data, bytes):
                resp_tid = int(''.join(re.findall('..', str(bytes_response.data.hex()))[:2]), 16)
                req_dict = self._dicts_by_tid[resp_tid]
                deserialized_dict = user_response_deserialize(bytes_response.data, req_dict)
                self._pending_responses[resp_tid].set_result(deserialized_dict)
