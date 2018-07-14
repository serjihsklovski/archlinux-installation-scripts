import os


def mount(device: str, directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    os.system('mount "{device}" {directory}'.format(device=device, directory=directory))


def swapon(device: str):
    os.system('swapon "{device}"'.format(device=device))
