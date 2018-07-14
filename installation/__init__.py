import os
import subprocess


def set_mirrors(mirrors: list):
    # backup the current mirrorlist
    date = subprocess.check_output('date -u +%F_%H-%M-%S')
    os.system('copy /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.{date}'.format(date=date))

    os.system('> /etc/pacman.d/mirrorlist')
    for mirror in mirrors:
        os.system('echo "Server = {mirror}" >> /etc/pacman.d/mirrorlist'.format(mirror=mirror))
