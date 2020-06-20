import json
import time
import threading
import websocket


def doitup(ws):
    data = {'command': 'auto_read'}

    while True:
        if data:
            ws.send(json.dumps(data))
            data = None
        time.sleep(1)
    ws.close()


def test_on_message(ws, message):
    print(message.rstrip())


def test_on_open(ws):
    t = threading.Thread(target=doitup, args=(ws,))
    t.daemon = True
    t.start()


# websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    'ws://127.0.0.1:1337/elbb_connect',
    on_message=test_on_message
)
ws.on_open = test_on_open
ws.run_forever()
