import asyncio
import aiohttp.web
import contextlib
import json
import sys


conf = {
    'ws': {
        'host': '0.0.0.0',
        'port': 3456},
    'modbus': {
        'host': 'localhost',
        'port': 502}}


async def ws_handler(request):
    #breakpoint()
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    try:
        print("Connection established.")
        # conn_msg_str = await ws.receive_str()
        # conn_msg = json.loads(conn_msg_str)

        reader, writer = await asyncio.open_connection(
            conf['modbus']['host'], conf['modbus']['port'])
    except Exception as e:
        #breakpoint()
        return ws
    await ws.send_str('ACK')

    async def tcp_read_loop():
        while True:
            try:
                msg = await reader.read(1024)
            except Exception:
                break
            if not msg:
                break
            await ws.send_bytes(msg)

    async def ws_read_loop():
        while True:
            try:
                msg = await ws.receive_bytes()
            except Exception:
                break
            writer.write(msg)

    tcp_future = asyncio.ensure_future(tcp_read_loop())
    ws_future = asyncio.ensure_future(ws_read_loop())
    await asyncio.wait(
        [tcp_future, ws_future], return_when=asyncio.FIRST_COMPLETED)
    tcp_future.cancel()
    ws_future.cancel()

    with contextlib.suppress(Exception):
        writer.write_eof()
    with contextlib.suppress(Exception):
        writer.close()
    return ws


def main():
    app = aiohttp.web.Application()
    app.router.add_route('*', '/ws', ws_handler)
    aiohttp.web.run_app(app,
                        host=conf['ws']['host'], port=conf['ws']['port'],
                        shutdown_timeout=0)

if __name__ == '__main__':
    sys.exit(main())
