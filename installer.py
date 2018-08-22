import re
from typing import Iterable, List, Generator

import format
import mnt_devs
import sgdisk
from command_runner import CommandRunner, SystemCommandRunner, SystemListCommandRunner
from sgdisk import SizeUnit, PartitionType

_SIZE_POSTFIX_TO_UNIT = {
    'MB': SizeUnit.MEGABYTES,
    'GB': SizeUnit.GIGABYTES,
}


def _set_ntp() -> CommandRunner:
    return SystemListCommandRunner([
        'timedatectl set-ntp true',
        'timedatectl status',
    ])


def _parse_size_and_unit_postfix(size: str) -> tuple:
    pattern = re.compile(r'^(?P<size_value>\d+)(?P<size_unit>(MB)|(GB))$')
    matcher = pattern.search(size)
    if matcher is None:
        raise Exception('Wrong format of partition size: you must specify the number and the unit postfix.')
    return int(matcher.group('size_value')), _SIZE_POSTFIX_TO_UNIT[matcher.group('size_unit')]


def _perform_disk_partitioning(device: str, partitions: List[map]) -> Generator:
    sgdisk.set_device(device)
    yield sgdisk.clear()
    yield sgdisk.convert_mbr_to_gpt()

    for partition in partitions[:-1]:
        size, size_unit = _parse_size_and_unit_postfix(partition['size'])
        yield sgdisk.create_partition(size, size_unit, PartitionType[partition['type']], partition['name'])

    if len(partitions) > 1:
        partition = partitions[-1]
        yield sgdisk.create_partition_as_rest(PartitionType[partition['type']], partition['name'])

    yield sgdisk.print_table()


def _perform_disk_formatting(partitions: Iterable[map]) -> Generator:
    format_map = {
        'fat32': format.fat32,
        'ext4': format.ext4,
        'swap': format.swap,
    }

    for partition in partitions:
        format_attr = partition['format']
        func = format_map[format_attr['fs']]
        yield func(format_attr['device'], format_attr['label'])


def _perform_devices_mounting(mount_config: Iterable[map]) -> Generator:
    for mc in mount_config:
        if 'dir' in mc:
            yield SystemCommandRunner('[ -d "{directory}" ] || mkdir -p "{directory}"'.format(directory=mc['dir']))
            yield mnt_devs.mount(mc['device'], mc['dir'])
        elif mc['swap']:
            yield mnt_devs.swapon(mc['device'])


def _set_mirrors(mirrors: Iterable[str]) -> Generator:
    # backup the current mirrorlist
    yield SystemCommandRunner('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.{date}'.format(
        date='$(date +%F_%T | sed -e "s/:/-/g")'))

    # clear the file
    yield SystemCommandRunner('> /etc/pacman.d/mirrorlist')
    for mirror in mirrors:
        yield SystemCommandRunner('echo "Server = {mirror}" >> /etc/pacman.d/mirrorlist'.format(mirror=mirror))


def _pacstrap(path: str, groups: Iterable[str]) -> CommandRunner:
    return SystemCommandRunner('pacstrap "{path}" {groups}'.format(path=path, groups=' '.join(groups)))


def _genfstab(mountpoint: str, fstab_file: str):
    return SystemCommandRunner('genfstab -t UUID "{mountpoint}" >> "{fstab_file}"'.format(mountpoint=mountpoint,
                                                                                          fstab_file=fstab_file))


def gen_command_runners(config) -> Generator:
    yield _set_ntp()
    yield from _perform_disk_partitioning(config['device'], config['partitions'])
    yield from _perform_disk_formatting(config['partitions'])
    yield from _perform_devices_mounting(config['mount'])
    yield from _set_mirrors(config['mirrors'])
    yield _pacstrap(config['pacstrap']['path'], config['pacstrap']['groups'])
    yield _genfstab(config['genfstab']['mountpoint'], config['genfstab']['fstab-file'])
