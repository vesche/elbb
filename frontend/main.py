#!/usr/bin/env python

import json
import redis

from flask import Flask, request, render_template
from concurrent.futures import ThreadPoolExecutor

from client import Bot

app = Flask('elbb-client')
executor = ThreadPoolExecutor(2)

redis_controller = redis.Redis(host='localhost', port=6379, db=0)
redis_controller.delete('command')
redis_controller.delete('messages')

with open('my.json', 'r') as f:
    bots = json.loads(f.read())

# dict for storing Bot websocket handlers
bot_controllers = dict()


@app.route('/')
def index():
    return render_template('index.html', bots=bots)


@app.route('/bot/<bot_name>')
def bot(bot_name):
    # start a new bot
    bot_data = bots[bot_name]
    new_bot = Bot(bot_name, bot_data)
    bot_controllers[bot_name] = new_bot
    executor.submit(new_bot.start, redis_controller)
    return render_template('bot.html', bot_data=bot_data)


@app.route('/command', methods=['POST'])
def command():
    redis_controller.set('command', request.form['command'])
    return ('', 204)


@app.route('/messages')
def messages():
    m_tmp = str()

    while True:    
        m = redis_controller.lpop('messages')
        if not m:
            break
        m_tmp += m.decode('utf-8') + ' | '

    return m_tmp.rstrip(' | ')


if __name__ == '__main__':
    app.run()
