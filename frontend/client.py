import json
import time
import redis
import threading
import websocket


class Bot:
    def __init__(self, bot_name, bot_data):
        self.name = bot_name
        self.ip = bot_data['ip']
        self.username = bot_data['username']
        self.password = bot_data['password']
        self.ws = None

    def start(self, redis_controller):
        def run_bot(ws):
            while True:
                command = redis_controller.get('command')

                if command:
                    args = dict()
                    command = command.decode('utf-8')

                    if command == 'auto_login':
                        args = {
                            'username': self.username,
                            'password': self.password
                        }

                    payload = json.dumps({
                        'command': command,
                        'args': args
                    })
                    ws.send(payload)
                    redis_controller.delete('command')

                # wait until redis "command" updates
                time.sleep(1)

            # on disconnect, close websocket and remove bot from bots dict
            ws.close()
            bots.pop(self.name)

        def on_message(ws, message):
            redis_controller.lpush('messages', message.rstrip())

        def on_open(ws):
            bot_thread = threading.Thread(target=run_bot, args=(ws,))
            bot_thread.daemon = True
            bot_thread.start()

        self.ws = websocket.WebSocketApp(
            f'ws://{self.ip}:51337/elbb_connect',
            on_message=on_message
        )
        self.ws.on_open = on_open
        self.ws.run_forever()
