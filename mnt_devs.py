from command_runner import CommandRunner, SystemCommandRunner


def mount(device: str, directory) -> CommandRunner:
    return SystemCommandRunner('mount "{device}" {directory}'.format(device=device, directory=directory))


def swapon(device: str) -> CommandRunner:
    return SystemCommandRunner('swapon "{device}"'.format(device=device))
