from command_runner import CommandRunner, SystemCommandRunner


def fat32(device: str, label: str) -> CommandRunner:
    return SystemCommandRunner('mkfs.fat -F32 "{device}" -n "{label}"'.format(device=device, label=label.upper()))


def ext4(device: str, label: str) -> CommandRunner:
    return SystemCommandRunner('mkfs.ext4 "{device}" -L "{label}"'.format(device=device, label=label))


def swap(device: str, label: str) -> CommandRunner:
    return SystemCommandRunner('mkswap "{device}" -L "{label}"'.format(device=device, label=label))
