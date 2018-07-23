import os
import subprocess


class CommandRunner:

    def __init__(self, code, runner):
        self._code = code
        self._runner = runner

    def run(self):
        self._runner(self._code)


def run_in_system(code: str):
    os.system(code)


def run_handling_output(code: list, output_handler):
    output = subprocess.check_output(code)
    output_handler(output)


def run_all_in_system(commands: list):
    for command in commands:
        run_in_system(command)
