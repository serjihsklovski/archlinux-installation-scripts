from argparse import ArgumentParser

import config_loader
import installer

DEFAULT_CONFIG_PATH = './installation.config.json'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args()

    config = config_loader.load(args.file)

    installer.set_ntp()
    installer.perform_disk_partitioning(config['device'], config['partitions'])
    installer.perform_disk_formatting(config['partitions'])
    installer.perform_devices_mounting(config['mount'])
    installer.set_mirrors(config['mirrors'])
    installer.pacstrap(config['pacstrap']['path'], config['pacstrap']['groups'])
    installer.genfstab(config['genfstab']['mountpoint'], config['genfstab']['fstab-file'])
