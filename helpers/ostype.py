import platform


class OSType:
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'


def get_os() -> OSType:
    return platform.system().lower()
