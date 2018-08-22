from enum import Enum, auto
from functools import lru_cache

from command_runner import CommandRunner, OutputHandlingCommandRunner


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

_device: str = None


def _handle_output_not_success(output: bytes):
    if not output.decode('utf-8').endswith(_SUCCESS_OUTPUT):
        raise Exception('The operation was completed improperly.')


def _handle_output_print(output: bytes):
    print(output.decode('utf-8'))


def set_device(device: str):
    global _device
    _device = device


def get_device():
    return _device


def clear() -> CommandRunner:
    return OutputHandlingCommandRunner(
        ['sgdisk', '--clear', get_device()],
        _handle_output_not_success,
    )


def convert_mbr_to_gpt() -> CommandRunner:
    return OutputHandlingCommandRunner(
        ['sgdisk', '--mbrtogpt', get_device()],
        _handle_output_not_success
    )


def create_partition(size: int, size_unit: SizeUnit, partition_type: PartitionType, name: str) -> CommandRunner:
    new_partition = '--new=0:0:+{size}{size_unit} --typecode=0:{type_code} --change-name=0:"{name}"'.format_map({
        'size': size,
        'size_unit': SizeUnit.get_value(size_unit),
        'type_code': PartitionType.get_value(partition_type),
        'name': name,
    })

    return OutputHandlingCommandRunner(
        ['sgdisk', new_partition, get_device()],
        _handle_output_not_success
    )


def create_partition_as_rest(partition_type: PartitionType, name: str) -> CommandRunner:
    new_partition = '--new=0:0:0 --typecode=0:{type_code} --change-name=0:"{name}"'.format_map({
        'type_code': PartitionType.get_value(partition_type),
        'name': name,
    })

    return OutputHandlingCommandRunner(
        ['sgdisk', new_partition, get_device()],
        _handle_output_not_success
    )


def print_table() -> CommandRunner:
    return OutputHandlingCommandRunner(
        ['sgdisk', '--print', get_device()],
        _handle_output_print
    )


if __name__ == '__main__':
    assert SizeUnit.get_value(SizeUnit.MEGABYTES) == 'M', '`SizeUnit.MEGABYTES` should be "M"'
    assert SizeUnit.get_value(SizeUnit.GIGABYTES) == 'G', '`SizeUnit.GIGABYTES` should be "G"'

    assert PartitionType.get_value(PartitionType.EFI) == 'ef00', '`PartitionType.EFI` should be "ef00"'
    assert PartitionType.get_value(PartitionType.ROOT) == '8300', '`PartitionType.ROOT` should be "8300"'
    assert PartitionType.get_value(PartitionType.SWAP) == '8200', '`PartitionType.SWAP` should be "8200"'
    assert PartitionType.get_value(PartitionType.HOME) == '8300', '`PartitionType.HOME` should be "8300"'
