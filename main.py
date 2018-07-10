import config_loader
import sgdisk
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', required=True)

    args = parser.parse_args()

    config = config_loader.load(args.file)

    device = config['device']
    sgdisk.set_device(device)
    sgdisk.print_table()
