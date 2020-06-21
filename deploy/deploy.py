#!/usr/bin/env python

import sys
import json
import time
import crayons
import getpass

from fabric import Connection, Config
from linode_api4 import LinodeClient

BAR = '='*40
DEBUG = False

try:
    with open('my.json') as f:
        DEPLOY = json.loads(f.read())
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print('Error, deploy.json is invalid or not found!')
    sys.exit(1)


def run_command(conn, description, command):
    print(crayons.yellow(f'[~] Running "{description}"'))

    if 'sudo' in command:
        result = conn.sudo(command, hide=True)
    else:
        result = conn.run(command, hide=True)

    # log
    with open('deploy.log', 'a') as f:
        f.write(
            f'{BAR}\n' + \
            f'Command: {command}\n' + \
            f'Description: {description}\n' + \
            f'Success: {result.ok}\n' + \
            f'Output:\n{result.stdout}\n'
        )

    if result.ok:
        print(crayons.green(f'[+] SUCCESS: {description}'))
    else:
        print(crayons.red(f'[-] ERROR: {description}'))


def create_instance():
    client = LinodeClient(DEPLOY['api_key'])
    linode_server, root_password = client.linode.instance_create(
        'g6-dedicated-2',
        'us-central',
        image='linode/arch',
        label=DEPLOY['name']
    )
    print(crayons.green(f'[+] Created new Linode instance "{linode_server.label}"!'))
    if DEBUG:
        print('[!] IP:', linode_server.ipv4[0])
        print('[!] RP:', root_password)
    return (linode_server, linode_server.ipv4[0], root_password)


def wait_for_instance(linode_instance):
    status = linode_instance.status
    while status != 'running':
        print(crayons.yellow(f'[~] Waiting for {linode_instance.label} to start up, currently {status}...'))
        time.sleep(5)
        status = linode_instance.status


def init_config_instance(ip, root_password):
    conn = Connection(
        host=ip,
        user='root',
        port=22,
        connect_kwargs={'password': root_password}
    )
    run_command(
        conn,
        'Full system update',
        'pacman -Syyu --noconfirm'
    )
    run_command(
        conn,
        'Install required packages',
        'pacman -S rxvt-unicode git redis tigervnc xfce4 binutils fakeroot gcc pkgconf make zenity python-pip tk scrot which tesseract go perl-file-pushd sdl2_net sdl2_image openal glu unzip patch --noconfirm'
    )
    run_command(
        conn,
        'Set hostname',
        f'hostnamectl set-hostname {DEPLOY["hostname"]}'
    )
    run_command(
        conn,
        'Add user',
        f'useradd -m -G wheel -s /bin/bash {DEPLOY["username"]}'
    )
    run_command(
        conn,
        'Set user password',
        f'echo -e "{DEPLOY["password"]}\n{DEPLOY["password"]}" | (passwd {DEPLOY["username"]})'
    )
    run_command(
        conn,
        'Create /usr/share/tessdata directory',
        'mkdir -p /usr/share/tessdata/'
    )
    conn.put('files/sudoers', '/etc/sudoers')
    conn.put('files/sshd_config', '/etc/ssh/sshd_config')
    conn.put('files/eng.traineddata', '/usr/share/tessdata/')


def config_instance(ip):
    config = Config(overrides={'sudo': {'password': DEPLOY['password']}})
    conn = Connection(
        host=ip,
        user=DEPLOY['username'],
        port=DEPLOY['ssh_port'],
        connect_kwargs={'password': DEPLOY['password']},
        config=config
    )
    run_command(
        conn,
        'SSH iptables command 1',
        f'sudo iptables -A INPUT -p tcp --dport {DEPLOY["ssh_port"]} --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'SSH iptables command 2',
        f'sudo iptables -A INPUT -p tcp --dport {DEPLOY["ssh_port"]} -j DROP'
    )
    run_command(
        conn,
        'VNC iptables command 1',
        f'sudo iptables -A INPUT -p tcp --dport 5901 --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'VNC iptables command 2',
        f'sudo iptables -A INPUT -p tcp --dport 5901 -j DROP'
    )
    run_command(
        conn,
        'elbb iptables command 1',
        f'sudo iptables -A INPUT -p tcp --dport 51337 --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'elbb iptables command 2',
        f'sudo iptables -A INPUT -p tcp --dport 51337 -j DROP'
    )
    run_command(
        conn,
        'Start redis',
        'sudo systemctl start redis'
    )
    run_command(
        conn,
        'Enable redis',
        'sudo systemctl enable redis'
    )
    run_command(
        conn,
        'Create VNC directory',
        'mkdir ~/.vnc'
    )
    run_command(
        conn,
        'Create VNC passwd file',
        f'echo {DEPLOY["password"]} | vncpasswd -f > ~/.vnc/passwd'
    )
    run_command(
        conn,
        'Modify VNC passwd file permissions',
        f'chmod 600 ~/.vnc/passwd'
    )
    conn.put('files/xstartup', '.vnc/')
    run_command(
        conn,
        'Mark xstartup as an executable',
        'chmod +x ~/.vnc/xstartup'
    )
    run_command(
        conn,
        'Start VNC server',
        'vncserver'
    )
    run_command(
        conn,
        'Download cal3d snapshot from AUR',
        'curl -O https://aur.archlinux.org/cgit/aur.git/snapshot/cal3d.tar.gz'
    )
    run_command(
        conn,
        'Download gameclient snapshot from AUR',
        f'curl -O {DEPLOY["gameclient_url"]}'
    )
    run_command(
        conn,
        'Extract cal3d',
        'tar xzvf cal3d.tar.gz'
    )
    run_command(
        conn,
        'Extract gameclient',
        f'tar xzvf {DEPLOY["gameclient"]}.tar.gz'
    )
    run_command(
        conn,
        'Build cal3d',
        'pushd cal3d/ && makepkg -s --noconfirm'
    )
    run_command(
        conn,
        'Install cal3d',
        'sudo pacman -U cal3d/cal3d-*.tar.xz --noconfirm'
    )
    run_command(
        conn,
        'Build gameclient',
        f'pushd {DEPLOY["gameclient"]}/ && makepkg -s --noconfirm'
    )
    run_command(
        conn,
        'Install gameclient',
        f'sudo pacman -U {DEPLOY["gameclient"]}/{DEPLOY["gameclient"]}-*.tar.xz --noconfirm'
    )
    run_command(
        conn,
        'Clone elbb',
        'git clone https://github.com/vesche/elbb'
    )
    run_command(
        conn,
        'Install elbb',
        'pushd elbb/ && python setup.py install --user'
    )

    with open('files/bashrc', 'r') as f:
        data = f.read()
    with open('files/bashrc', 'w') as f:
        f.write(data.replace('gameclient', DEPLOY['gameclient']))

    conn.put('files/bashrc', '.bashrc')

    run_command(
        conn,
        'Clean up',
        f'rm -rf *.tar.gz cal3d/ {DEPLOY["gameclient"]}/'
    )


def main():
    # create new instance
    linode_server, ip, root_password = create_instance()

    # ensure instance is running
    wait_for_instance(linode_server)

    # conduct initial configuration of instance
    init_config_instance(ip, root_password)

    # reboot instance
    linode_server.reboot()
    wait_for_instance(linode_server)

    # configure instance
    config_instance(ip)

    print('''
    Manually configure gameclient:
    v: 1152x864x16, fps 8, g 1.00, wsq 0, disable all
    g: disable all, 256, sud 15, pp 30, mef 20.00/15.00, lct 16, micps 1
    h: wot, uowb
    save configuration
    ''')

    print(f'''
    Finished deployment! :D
    Name: {linode_server.label}
    VNC: {ip}:1
    ''')


if __name__ == '__main__':
    main()
