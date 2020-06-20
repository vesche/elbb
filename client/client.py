import json
import time
import redis
import threading
import websocket

r = redis.Redis(host='localhost', port=6379, db=0)


def run_bot(ws):
    while True:
        command = r.get('command')
        if command:
            ws.send(json.dumps({'command': command.decode('utf-8')}))
            r.delete('command')
        time.sleep(1)
    ws.close()


def on_message(ws, message):
    # do things...
    print(message.rstrip())


def on_open(ws):
    t = threading.Thread(target=run_bot, args=(ws,))
    t.daemon = True
    t.start()


def start_bot(ip):
    ws = websocket.WebSocketApp(
        f'ws://{ip}:1337/elbb_connect',
        on_message=on_message
    )
    ws.on_open = on_open
    ws.run_forever()
