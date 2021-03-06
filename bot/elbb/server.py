"""elbb.server"""

import json
import asyncio
import threading

from elbb.meta import BANNER
from elbb.playbooks import manifest
from elbb.engine import launch_client
from elbb.queue import get_queue, clear_queue

from sanic import Sanic, response
from sanic.websocket import WebSocketProtocol

app = Sanic(name='elbb')


async def _consumer_handler(ws):
    while True:
        data = await ws.recv()
        data = json.loads(data)

        target_func = None
        command = data['command']
        args = data['args']

        # get target function from playbook manifest 
        if command in manifest:
            target_func = manifest[command]

        if target_func:
            t = threading.Thread(target=target_func, args=[*args.values()])
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
    # launch game client (if it's not already running)
    launch_client()

    while True:
        consumer_task = asyncio.ensure_future(_consumer_handler(ws))
        producer_task = asyncio.ensure_future(_producer_handler(ws))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


def start_server():
    app.run('0.0.0.0', port=51337, protocol=WebSocketProtocol)
