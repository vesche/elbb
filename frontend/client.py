import json
import time
import redis
import threading
import websocket

r = redis.Redis(host='localhost', port=6379, db=0)

username = str()
password = str()


def run_bot(ws):
    global username
    global password

    while True:
        command = r.get('command')

        if command:
            args = dict()

            command = command.decode('utf-8')
            if command == 'auto_login':
                args = {
                    'username': username,
                    'password': password
                }

            payload = json.dumps({
                'command': command,
                'args': args
            })
            ws.send(payload)
            r.delete('command')
        time.sleep(1)

    ws.close()


def on_message(ws, message):
    r.lpush('messages', message.rstrip())


def on_open(ws):
    t = threading.Thread(target=run_bot, args=(ws,))
    t.daemon = True
    t.start()


def start_bot(bot_data):
    global username
    global password
    username = bot_data['username']
    password = bot_data['password']

    ws = websocket.WebSocketApp(
        f'ws://{bot_data["ip"]}:51337/elbb_connect',
        on_message=on_message
    )
    ws.on_open = on_open
    ws.run_forever()
