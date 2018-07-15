import os
import datetime


def set_mirrors(mirrors: list):
    # backup the current mirrorlist
    utc_date_formatted = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

    os.system('copy /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.{date}'.format(date=utc_date_formatted))

    os.system('> /etc/pacman.d/mirrorlist')
    for mirror in mirrors:
        os.system('echo "Server = {mirror}" >> /etc/pacman.d/mirrorlist'.format(mirror=mirror))
