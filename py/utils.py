import platform
import os
import getpass

WIN = 'Windows'
WIN_M2 = 'C:\\Users\\{}\\.m2'
LINUX_M2 = '/home/{}/.m2'

def get_m2():
    if get_os() == WIN:
        return WIN_M2.format(get_user())
    else:
        return LINUX_M2.format(get_user())

def get_os():
    return platform.system()

def get_user():
    return getpass.getuser()

def path_join(path, *paths):
    return os.path.join(path, *paths)

def exists(path):
    return os.path.exists(path)