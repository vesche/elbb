"""elbb.server"""

import json
import asyncio
import threading

from elbb.meta import BANNER
from elbb.engine import launch_client
from elbb.queue import get_queue, clear_queue
from elbb.playbooks import start_auto_fire_essence, auto_read

from sanic import Sanic, response
from sanic.websocket import WebSocketProtocol

app = Sanic(name='elbb')


async def _consumer_handler(ws):
    # launch game client if it's not already
    launch_client()

    while True:
        data = await ws.recv()
        data = json.loads(data)

        target_func = None
        command = data['command']

        if command == 'noop':
            continue
        elif command == 'auto_fire_essence':
            target_func = start_auto_fire_essence
        elif command == 'auto_read':
            target_func = auto_read

        if target_func:
            t = threading.Thread(target=target_func)
            t.daemon = True
            t.start()


async def _producer_handler(ws):
    queue = get_queue()
    clear_queue()

    if queue:
        await ws.send(queue)
    await asyncio.sleep(.1)


@app.websocket('/elbb_connect')
async def elbb_connect(request, ws):
    while True:
        consumer_task = asyncio.ensure_future(_consumer_handler(ws))
        producer_task = asyncio.ensure_future(_producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


def start():
    print(BANNER)
    app.run('0.0.0.0', port=51337, protocol=WebSocketProtocol)
