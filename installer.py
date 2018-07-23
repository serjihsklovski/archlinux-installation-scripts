import os
import re
import datetime

import format
import mnt_devs
import sgdisk
from sgdisk import SizeUnit, PartitionType

_SIZE_POSTFIX_TO_UNIT = {
    'MB': SizeUnit.MEGABYTES,
    'GB': SizeUnit.GIGABYTES,
}


def set_ntp():
    os.system('timedatectl set-ntp true')
    os.system('timedatectl status')


def _parse_size_and_unit_postfix(size: str) -> tuple:
    pattern = re.compile(r'^(?P<size_value>\d+)(?P<size_unit>(MB)|(GB))$')
    matcher = pattern.search(size)
    if matcher is None:
        raise Exception('Wrong format of partition size: you must specify the number and the unit postfix.')
    return int(matcher.group('size_value')), _SIZE_POSTFIX_TO_UNIT[matcher.group('size_unit')]


def perform_disk_partitioning(device: str, partitions: list):
    sgdisk.set_device(device)
    sgdisk.clear()
    sgdisk.convert_mbr_to_gpt()

    for partition in partitions[:-1]:
        size, size_unit = _parse_size_and_unit_postfix(partition['size'])
        sgdisk.create_partition(size, size_unit, PartitionType[partition['type']], partition['name'])

    if len(partitions) > 1:
        partition = partitions[-1]
        sgdisk.create_partition_as_rest(PartitionType[partition['type']], partition['name'])

    sgdisk.print_table()


def perform_disk_formatting(partitions: list):
    format_map = {
        'fat32': format.fat32,
        'ext4': format.ext4,
        'swap': format.swap,
    }

    for partition in partitions:
        format_attr = partition['format']
        func = format_map[format_attr['fs']]
        func(format_attr['device'], format_attr['label'])


def perform_devices_mounting(mount_config: list):
    for mc in mount_config:
        if 'dir' in mc:
            mnt_devs.mount(mc['device'], mc['dir'])
        elif mc['swap']:
            mnt_devs.swapon(mc['device'])


def set_mirrors(mirrors: list):
    # backup the current mirrorlist
    utc_date_formatted = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

    os.system('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.{date}'.format(date=utc_date_formatted))

    os.system('> /etc/pacman.d/mirrorlist')
    for mirror in mirrors:
        os.system('echo "Server = {mirror}" >> /etc/pacman.d/mirrorlist'.format(mirror=mirror))


def pacstrap(path: str, groups: list):
    os.system('pacstrap {path} {groups}'.format(path=path, groups=' '.join(groups)))


def genfstab(mountpoint: str, fstab_file: str):
    os.system('genfstab -t UUID {mountpoint} >> {fstab_file}'.format(mountpoint=mountpoint, fstab_file=fstab_file))