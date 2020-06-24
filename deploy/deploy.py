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
    # give the instance time to start services
    time.sleep(10)


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
        'pacman -S xorg-server-xvfb x11vnc rxvt-unicode git redis binutils fakeroot gcc pkgconf make zenity python-pip tk scrot which tesseract go perl-file-pushd sdl2_net sdl2_image openal glu unzip patch --noconfirm'
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
    conn.put('files/environment', '/etc/environment')
    conn.put('files/eng.traineddata', '/usr/share/tessdata/')

    conn.put('files/xvfb@.service', '/etc/systemd/system')
    run_command(
        conn,
        'Enable xvfb service on :99',
        'systemctl enable xvfb@:99.service'
    )

    conn.put('files/x11vnc@.service', '/etc/systemd/system')
    run_command(
        conn,
        'Enable x11vnc service on :99',
        'systemctl enable x11vnc@:99.service'
    )

    run_command(
        conn,
        'Run a systemd daemon reload',
        'systemctl daemon-reload'
    )

    # disable ipv6
    conn.put('files/grub', '/etc/default/grub')
    run_command(
        conn,
        'Update GRUB with IPv6 disabled',
        'grub-mkconfig -o /boot/grub/grub.cfg'
    )


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
        'Set iptables SSH (1/2)',
        f'sudo iptables -A INPUT -p tcp --dport {DEPLOY["ssh_port"]} --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'Set iptables SSH (2/2)',
        f'sudo iptables -A INPUT -p tcp --dport {DEPLOY["ssh_port"]} -j DROP'
    )
    run_command(
        conn,
        'Set iptables VNC (1/2)',
        f'sudo iptables -A INPUT -p tcp --dport 5901 --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'Set iptables VNC (2/2)',
        f'sudo iptables -A INPUT -p tcp --dport 5901 -j DROP'
    )
    run_command(
        conn,
        'Set iptables elbb (1/2)',
        f'sudo iptables -A INPUT -p tcp --dport 51337 --source {DEPLOY["src_ip"]}/32 -j ACCEPT'
    )
    run_command(
        conn,
        'Set iptables elbb (1/2)',
        f'sudo iptables -A INPUT -p tcp --dport 51337 -j DROP'
    )
    run_command(
        conn,
        'Save iptables rules',
        'sudo iptables-save | sudo tee /etc/iptables/iptables.rules'
    )
    run_command(
        conn,
        'Start iptables service',
        'sudo systemctl start iptables'
    )
    run_command(
        conn,
        'Enable iptables service',
        'sudo systemctl enable iptables'
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
        'Download dtach snapshot from AUR',
        'curl -O https://aur.archlinux.org/cgit/aur.git/snapshot/dtach.tar.gz'
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
        'Extract dtach',
        'tar xzvf dtach.tar.gz'
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
        'Build dtach',
        'pushd dtach/ && makepkg -s --noconfirm'
    )
    run_command(
        conn,
        'Install dtach',
        'sudo pacman -U dtach/dtach-*.tar.xz --noconfirm'
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
    run_command(
        conn,
        'Create an .Xauthority file',
        'touch .Xauthority'
    )

    with open('files/bashrc', 'r') as f:
        data = f.read()
    with open('files/bashrc', 'w') as f:
        f.write(data.replace('gameclient', DEPLOY['gameclient']))
    conn.put('files/bashrc', '.bashrc')
    # revert
    with open('files/bashrc', 'w') as f:
        f.write(data)

    run_command(
        conn,
        'Start the game client',
        f'dtach -n /tmp/foo xvfb-run {DEPLOY["gameclient"]}'
    )
    run_command(
        conn,
        'Wait for the game client to start',
        'sleep 20'
    )
    conn.put('files/post_deploy.py', 'post_deploy.py')
    run_command(
        conn,
        'Run post deployment script',
        'python post_deploy.py'
    )
    run_command(
        conn,
        'Clean up deployment',
        f'rm -rf post_deploy.py *.tar.gz dtach/ cal3d/ {DEPLOY["gameclient"]}/'
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
    print(crayons.green(f'[+] Rebooting: {linode_server.label}'))
    wait_for_instance(linode_server)

    # configure instance
    config_instance(ip)

    print('''
    Change options:
    HUD:
        - Use Opaque Window Backgrounds
    Video:
        - 1024x768x32
        - Limit FPS: 8
    Save options
    ''')

    print(f'''
    Finished deployment! :D
    Name: {linode_server.label}
    x11vnc: {ip}:1
    ''')


if __name__ == '__main__':
    main()
