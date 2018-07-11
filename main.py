import config_loader
import sgdisk
from argparse import ArgumentParser


def do_disk_partitioning(device: str):
    sgdisk.set_device(device)
    sgdisk.clear()
    sgdisk.convert_mbr_to_gpt()
    sgdisk.print_table()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()

    config = config_loader.load(args.file)

    do_disk_partitioning(config['device'])
