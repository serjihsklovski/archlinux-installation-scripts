import os


_device = None


def _sgdisk_wrapper(device_getter):
    def wrap1(sgdisk_cmd):
        def wrap2():
            return os.system('sgdisk {cmd} {device}'.format(cmd=sgdisk_cmd(), device=device_getter()))
        return wrap2
    return wrap1


def set_device(device: str):
    global _device
    _device = device


def get_device():
    return _device


@_sgdisk_wrapper(get_device)
def print_table():
    return '--print'
