import os
import json

from fabric import Connection

with open('my.json') as f:
    config = json.loads(f.read())

conn = Connection(
    host=config['host'],
    user=config['user'],
    port=config['port'],
    connect_kwargs={'password': config['pass']}
)

conn.run('killall -q elbb', warn=True)
conn.run('pip uninstall elbb -y')
os.system('tar czf elbb.tar.gz ../../elbb/')
conn.put('elbb.tar.gz', 'elbb.tar.gz')
conn.run('tar xzf elbb.tar.gz')
conn.run('pushd elbb && python setup.py install --user')
# conn.run('dtach -n /tmp/foo .local/bin/elbb')
conn.run('rm -rf elbb.tar.gz elbb/')
os.system('rm elbb.tar.gz')