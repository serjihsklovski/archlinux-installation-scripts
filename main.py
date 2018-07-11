import config_loader
import sgdisk
import re
from argparse import ArgumentParser
from sgdisk import SizeUnit, PartitionType


SIZE_POSTFIX_TO_UNIT = {
    'MB': SizeUnit.MEGABYTES,
    'GB': SizeUnit.GIGABYTES,
}

DEFAULT_CONFIG_PATH = './installation.config.json'


def _parse_size_and_unit_postfix(size: str) -> tuple:
    pattern = re.compile(r'^(?P<size_value>\d+)(?P<size_unit>(MB)|(GB))$')
    matcher = pattern.search(size)
    if matcher is None:
        raise Exception('Wrong format of partition size: you must specify the number and the unit postfix.')
    return int(matcher.group('size_value')), SIZE_POSTFIX_TO_UNIT[matcher.group('size_unit')]


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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default=DEFAULT_CONFIG_PATH)

    args = parser.parse_args()

    config = config_loader.load(args.file)

    perform_disk_partitioning(config['device'], config['partitions'])
