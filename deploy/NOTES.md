# elbb Deployment notes

## elbb

* Linode
    * Arch Linux
    * Linode Dedicated 2 CPUs / 4GB RAM ($30/month)
* ssh root@ip
    * `pacman -Syyu && pacman -S rxvt-unicode`
        * exit, reboot in linode, re-ssh
        * notes: --noconfirm (when automating)
    * `useradd -m -G wheel -s /bin/bash user`
    * `hostnamectl set-hostname <hostname>`
    * `passwd user`
    * `vim /etc/sudoers`
        * uncomment wheel
    * `vim /etc/ssh/sshd_config`
        * change port
        * `AddressFamily inet # IPv4 only`
    * `systemctl restart sshd`
    * `systemctl stop systemd-resolved`
    * `systemctl disable systemd-resolved`

* ssh user@ip -p0
    * Only allow a certain IP
        * `sudo iptables -A INPUT -p tcp --dport <ssh_port> --source <src_ip>/32 -j ACCEPT`
        * `sudo iptables -A INPUT -p tcp --dport <ssh_port> -j DROP`
    * redis
        * `sudo pacman -S git redis`
        * `sudo systemctl start redis`
        * `sudo systemctl enable redis`
    * VNC
        * `sudo iptables -A INPUT -p tcp --dport 5901 --source <src_ip>/32 -j ACCEPT`
        * `sudo iptables -A INPUT -p tcp --dport 5901 -j DROP`
        * `sudo pacman -S tigervnc xfce4`
        * `vncserver`
        * `cp ~/.vnc/xstartup ~/.vnc/xstartup.bak`
        * `vim ~/.vnc/xstartup`
            * `#!/bin/bash`
            * `startxfce4 &`
        * `vncserver -kill :1`
        * `vncserver`
    * Game
        * `sudo pacman -S binutils fakeroot gcc pkgconf make zenity`
        * `curl -O https://aur.archlinux.org/cgit/aur.git/snapshot/yay.tar.gz`
        * `tar xzvf yay.tar.gz && cd yay/`
        * `makepkg -s`
        * `sudo pacman -U yay-*.tar.xz`
        * `yay -S <game>`
        * `<game>`
        * Run thru init
        * Change settings (v/g)
            * v: 1152x864x16, fps 8, g 1.00, wsq 0, disable all
            * g: disable all, 256, sud 15, pp 30, mef 20.00/15.00, lct 16, micps 1
            * h: wot, uowb
        * save
    * elbb
        * `git clone https://github.com/vesche/elbb && cd elbb/`
        * `sudo pacman -S pip tk scrot which tesseract`
        * `sudo cp tools/eng.traineddata /usr/share/tessdata`
        * `python setup.py install --user`
        * `vim ~/.bashrc`
            * `PATH=$PATH:~/.local/bin`
            * `GAMECLIENT='<game_executable>'`
        * `sudo iptables -A INPUT -p tcp --dport 51337 --source <src_ip>/32 -j ACCEPT`
        * `sudo iptables -A INPUT -p tcp --dport 51337 -j DROP`

## client

* TBD
* `sudo pacman -S tigervnc`
* `vncviewer` -> `<ip>:1`

## TODO

* gen ssh keys for easier access
* note: could run multiple VNC servers on a larger cloud VPS
