import os
import json

from invoke import Responder
from fabric import Connection

with open('my.json') as f:
    config = json.loads(f.read())

conn = Connection(
    host=config['host'],
    user=config['user'],
    port=config['port'],
    connect_kwargs={'password': config['pass']}
)

conn_root = Connection(
    host=config['host'],
    user='root',
    port=config['port'],
    connect_kwargs={'password': config['pass']}
)

conn_root.run('systemctl stop elbb')
conn.run('pip uninstall elbb -y')
os.system('tar czf bot.tar.gz ../bot/')
conn.put('bot.tar.gz', 'bot.tar.gz')
conn.run('tar xzf bot.tar.gz')
conn.run('pushd bot/ && python setup.py install --user')
conn_root.run('systemctl start elbb')
conn.run('rm -rf bot.tar.gz bot/')
os.system('rm bot.tar.gz')