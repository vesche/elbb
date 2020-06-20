#!/usr/bin/env python

import json
import redis

from flask import Flask, request, render_template
from concurrent.futures import ThreadPoolExecutor
# from flask_socketio import SocketIO, emit

from client import start_bot

app = Flask('elbb-client')
executor = ThreadPoolExecutor(2)

r = redis.Redis(host='localhost', port=6379, db=0)
r.delete('command')
r.delete('messages')


with open('my.json', 'r') as f:
    bots = json.loads(f.read())


@app.route('/')
def index():
    return render_template('index.html', bots=bots)


@app.route('/bot/<bot_name>')
def bot(bot_name):
    bot_data = bots[bot_name]
    executor.submit(start_bot, bot_data['ip'])
    return render_template('bot.html', bot_data=bot_data)


@app.route('/command', methods=['POST'])
def command():
    r.set('command', request.form['command'])
    return ('', 204)


@app.route('/messages')
def messages():
    m_tmp = str()

    while True:    
        m = r.lpop('messages')
        if not m:
            break
        m_tmp += m.decode('utf-8') + ' | '

    return m_tmp.rstrip(' | ')


if __name__ == '__main__':
    app.run()
