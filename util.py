from command_runner import SystemListCommandRunner, SystemCommandRunner, OutputHandlingCommandRunner


def gen_script_commands(command_runners: list) -> list:
    for commands in map(lambda cr: cr.get_code(), command_runners):
        for command in commands:
            yield command


# [TEST] `gen_script_commands`
if __name__ == '__main__':
    test_command_1 = 'test_command_1 --help'
    command_runner_1 = SystemCommandRunner(test_command_1)

    test_command_2 = ['test_command_2', '--verbose', '--param=value']
    command_runner_2 = OutputHandlingCommandRunner(test_command_2, lambda output: ...)

    test_command_3 = [
        'test_command_3 --help',
        'test_command_4 --version',
    ]
    command_runner_3 = SystemListCommandRunner(test_command_3)

    generator = gen_script_commands([command_runner_1, command_runner_2, command_runner_3])
    assert next(generator) == 'test_command_1 --help'
    assert next(generator) == 'test_command_2 --verbose --param=value'
    assert next(generator) == 'test_command_3 --help'
    assert next(generator) == 'test_command_4 --version'
    try:
        next(generator)
        raise AssertionError('Here you should catch `StopIteration`.')
    except StopIteration:
        pass
