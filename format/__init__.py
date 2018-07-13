import os


def _run_command(f):
    def wrap(*args, **kwargs):
        os.system(f(*args, **kwargs))
    return wrap


@_run_command
def fat32(device: str, label: str):
    return '/usr/bin/mkfs.fat -F32 "{device}" -n "{label}"'.format(device=device, label=label.upper())


@_run_command
def ext4(device: str, label: str):
    return '/usr/bin/mkfs.ext4 "{device}" --label="{label}"'.format(device=device, label=label)


@_run_command
def swap(device: str, label: str):
    return 'mkswap "{device}" --label="{label}"'.format(device=device, label=label)
