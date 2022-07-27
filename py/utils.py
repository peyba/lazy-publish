import platform
import os
import getpass
import sys
import xml.etree.ElementTree as et

import const

WIN = 'Windows'
WIN_M2 = 'C:\\Users\\{}\\.m2'
LINUX_M2 = '/home/{}/.m2'
M2_SETTINGS_FILE = 'settings.xml'
REP = 'repository'

def get_m2():
    if get_os() == WIN:
        return WIN_M2.format(get_user())
    else:
        return LINUX_M2.format(get_user())

def get_local_repository() -> str:
    m2_path = get_m2()
    m2_settings = os.path.join(m2_path, M2_SETTINGS_FILE)
    if (not os.path.exists(m2_settings)):
        return os.path.join(m2_path, REP)
    else:
        root = get_root(m2_settings, show_error=(__name__ == '__main__'))
        return root.findtext('./set:localRepository', namespaces=const.NAME_SPACE)

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

#===========================================================
# Generate part of m2 path to jar
# This is a project group path
# m2/repository/com/example_group/example_artifact/
#               ^^^^^^^^^^^^^^^^^
# example:
#   groupId is 'ru.app.utils'
#   return 'ru/app/utils' or 'ru\app\utils' depend on OS 
#
# params:
#   group_id - groupId tag text (str)
# return:
#   path (str)
#===========================================================
def get_group_path(group_id:str):
    path = ''
    for p in group_id.split('.'):
        path = path_join(path, p)
    return path

def del_last_char(text:str, char:str) -> str:
    if (len(char) > 1):
        raise Exception('Error! "{}" not a char'.format(char))
    txet = text[::-1]
    index = txet.find(char) + 1
    return text[0:len(text)-index] + text[len(text)-index + 1:]