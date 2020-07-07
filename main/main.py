import os
import asyncio
import aiohttp.web
import contextlib
import json
import sys
import subprocess
import socket
from multiprocessing import Process
import websocket


async def connect_to_socket():
    #
    # while True:
    #     msg = await ws.receive()
    #     if msg.tp == aiohttp.MsgType.text:
    #         if msg.data == 'close':
    #             await ws.close()
    #             break
    #         else:
    #             await ws.send_str(msg.data + '/answer')
    #     elif msg.tp == aiohttp.MsgType.closed:
    #         break
    #     elif msg.tp == aiohttp.MsgType.error:
    #         break

    for i in range (10):
        session = aiohttp.ClientSession()
        ws = await session.ws_connect('ws://localhost:3456/ws')
        await ws.send_bytes(b'000100000006090300040001')
        await ws.close()
        await session.close()


# async def write_loop():
# while True:
# ws.send_bytes(b'000100000006090300040001')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(connect_to_socket())
