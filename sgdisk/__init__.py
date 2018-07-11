import subprocess


_SUCCESS_OUTPUT = 'The operation has completed successfully.\n'

_device = None


def _handle_output_not_success(output: bytes):
    if output.decode('utf-8') != _SUCCESS_OUTPUT:
        raise Exception('The operation was completed improperly.')


def _handle_output_print(output: bytes):
    print(output.decode('utf-8'))


def _sgdisk_wrapper(device_getter, output_handler=_handle_output_not_success):
    def wrap1(sgdisk_cmd):
        def wrap2():
            output = subprocess.check_output('sgdisk {cmd} {device}'.format(cmd=sgdisk_cmd(), device=device_getter()),
                                             shell=True)
            return output_handler(output)
        return wrap2
    return wrap1


def set_device(device: str):
    global _device
    _device = device


def get_device():
    return _device


@_sgdisk_wrapper(get_device, output_handler=_handle_output_print)
def print_table():
    return '--print'


@_sgdisk_wrapper(get_device)
def clear():
    return '--clear'


@_sgdisk_wrapper(get_device)
def convert_mbr_to_gpt():
    return '--mbrtogpt'
