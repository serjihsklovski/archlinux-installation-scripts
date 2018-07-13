import subprocess


def fat32(device: str, label: str):
    subprocess.call('mkfs.fat -F32 "{device}" -n "{label}"'.format(device=device, label=label.upper()))


def ext4(device: str, label: str):
    subprocess.call('mkfs.ext4 "{device}" --label="{label}"'.format(device=device, label=label))


def swap(device: str, label: str):
    subprocess.call('mkswap "{device}" --label="{label}"'.format(device=device, label=label))
