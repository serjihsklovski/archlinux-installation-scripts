import subprocess


_file = None


def _run_command(output_handler=None):
    def wrap1(f):
        def wrap2(*args, **kwargs):
            output = subprocess.check_output(f(*args, **kwargs))
            if output_handler is not None:
                output_handler(output)
        return wrap2
    return wrap1


def log(output):
    print(output, file=_file)


@_run_command(output_handler=log)
def fat32(device: str, label: str):
    return '/usr/bin/mkfs.fat -F32 "{device}" -n "{label}"'.format(device=device, label=label.upper())


@_run_command(output_handler=log)
def ext4(device: str, label: str):
    return '/usr/bin/mkfs.ext4 "{device}" --label="{label}"'.format(device=device, label=label)


@_run_command(output_handler=log)
def swap(device: str, label: str):
    return 'mkswap "{device}" --label="{label}"'.format(device=device, label=label)
