import subprocess
from enum import Enum, auto
from functools import lru_cache


class SizeUnit(Enum):
    MEGABYTES = auto()
    GIGABYTES = auto()

    @classmethod
    @lru_cache(maxsize=None)
    def _get_values(cls) -> map:
        return {
            cls.MEGABYTES: 'M',
            cls.GIGABYTES: 'G',
        }

    @classmethod
    def get_value(cls, size_unit: 'SizeUnit') -> str:
        val = cls._get_values().get(size_unit)
        if val is None:
            raise Exception('Cannot recognize size unit: {size_unit}'.format(size_unit=size_unit))
        return val


class PartitionType(Enum):
    EFI = auto()
    ROOT = auto()
    SWAP = auto()
    HOME = auto()

    @classmethod
    @lru_cache(maxsize=None)
    def _get_values(cls) -> map:
        return {
            cls.EFI: 'ef00',
            cls.ROOT: '8300',
            cls.SWAP: '8200',
            cls.HOME: '8300',
        }

    @classmethod
    def get_value(cls, partition_type: 'PartitionType') -> str:
        val = cls._get_values().get(partition_type)
        if val is None:
            raise Exception('Cannot recognize partition type: {partition_type}'.format(partition_type=partition_type))
        return val


_SUCCESS_OUTPUT = 'The operation has completed successfully.\n'

_device = None


def _handle_output_not_success(output: bytes):
    if output.decode('utf-8') != _SUCCESS_OUTPUT:
        raise Exception('The operation was completed improperly.')


def _handle_output_print(output: bytes):
    print(output.decode('utf-8'))


def _sgdisk_wrapper(device_getter, output_handler=_handle_output_not_success):
    def wrap1(sgdisk_cmd):
        def wrap2(*args, **kwargs):
            output = subprocess.check_output(
                'sgdisk {cmd} {device}'.format(cmd=sgdisk_cmd(), device=device_getter(args, kwargs)), shell=True)
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


@_sgdisk_wrapper(get_device)
def create_partition(size: int, size_unit: SizeUnit, partition_type: PartitionType, name: str):
    return '--new=0:0:+{size}{size_unit} --typecode=0:{type_code} --change-name=0:"{name}"'.format_map({
        'size': size,
        'size_unit': SizeUnit.get_value(size_unit),
        'type_code': PartitionType.get_value(partition_type),
        'name': name,
    })


@_sgdisk_wrapper(get_device)
def create_partition_as_rest(partition_type: PartitionType, name: str):
    return '--new=0:0:0 --typecode=0:{type_code} --change-name=0:"{name}"'.format_map({
        'type_code': PartitionType.get_value(partition_type),
        'name': name,
    })


if __name__ == '__main__':
    assert SizeUnit.get_value(SizeUnit.MEGABYTES) == 'M', '`SizeUnit.MEGABYTES` should be "M"'
    assert SizeUnit.get_value(SizeUnit.GIGABYTES) == 'G', '`SuzeUnit.GIGABYTES` should be "G"'

    assert PartitionType.get_value(PartitionType.EFI) == 'ef00', '`PartitionType.EFI` should be "ef00"'
    assert PartitionType.get_value(PartitionType.ROOT) == '8300', '`PartitionType.ROOT` should be "8300"'
    assert PartitionType.get_value(PartitionType.SWAP) == '8200', '`PartitionType.SWAP` should be "8200"'
    assert PartitionType.get_value(PartitionType.HOME) == '8300', '`PartitionType.HOME` should be "8300"'
