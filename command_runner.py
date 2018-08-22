import os
import subprocess


class CommandRunner:

    def get_code(self) -> list:
        raise Exception('Operation is not supported.')

    def run(self):
        raise Exception('Operation is not supported.')


class SystemCommandRunner(CommandRunner):

    def __init__(self, command: str):
        self._command = command

    def get_code(self) -> list:
        return [self._command]

    def run(self):
        os.system(self._command)


class SystemListCommandRunner(CommandRunner):

    def __init__(self, commands: list):
        self._commands = commands

    def get_code(self) -> list:
        return self._commands

    def run(self):
        for command in self._commands:
            os.system(command)


class OutputHandlingCommandRunner(CommandRunner):

    def __init__(self, command_parts: list, output_handler):
        self._command_parts = command_parts
        self._output_handler = output_handler

    def get_code(self) -> list:
        return [' '.join(self._command_parts)]

    def run(self):
        output = subprocess.check_output(self._command_parts, shell=True)
        self._output_handler(output)
