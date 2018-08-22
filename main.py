import sys
from argparse import ArgumentParser

import config_loader
import installer
import util

_DEFAULT_CONFIG_PATH = './installation.config.json'
_DEFAULT_EXTRACT_OUTPUT = './install-archlinux.extracted.sh'


def _task_install(config):
    for command_runner in installer.gen_command_runners(config):
        command_runner.run()


def _task_extract(config, output):
    with open(output, 'w') as script:
        for command in util.gen_script_commands(installer.gen_command_runners(config)):
            print(command, file=script)


def main():
    parser = ArgumentParser()
    parser.add_argument('-t', '--task', default='install')
    parser.add_argument('-c', '--config_file', default=_DEFAULT_CONFIG_PATH)
    parser.add_argument('-o', '--output', default=_DEFAULT_EXTRACT_OUTPUT)
    args = parser.parse_args()

    config = config_loader.load(args.config_file)

    task = args.task
    if task == 'install':
        _task_install(config)
    elif task == 'extract':
        _task_extract(config, args.output)
    else:
        print('Could not find task {task}.'.format(task=task), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
