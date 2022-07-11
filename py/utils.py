import platform
import os
import getpass
import sys
import xml.etree.ElementTree as et

import const

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

def get_root(path:str, show_error:bool=False):
    if not exists(path):
        if show_error:
            sys.exit('Can\'t find {}'.format(path))
        else:
            return None

    return et.parse(path).getroot()

def get_pom_path(path:str) -> str:
    if path == None or path == '':
        pom_file = const.POM_FILE
    else:
        pom_file = path_join(path, const.POM_FILE)
    return pom_file