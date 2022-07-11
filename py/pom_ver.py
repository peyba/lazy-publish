from typing import List
from os.path import exists
import sys
import argparse
import xml.etree.ElementTree as et

import const
import utils

MODULE_NAME = 'version'

#===========================================================
# Return Maven app version (pom.xml/project/version)
# If parameter path is None or empty method use current 
# directory for search pom.xml
#
# params:
#   path - Path to the root Maven project directory (str)
# return:
#   version (str)
#===========================================================
def pom_ver(path:str) -> str:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
    if root != None:
        version = root.findtext('./pom:version', namespaces=const.NAME_SPACE)
        if version != None:
            return version

    return None

#===========================================================
# Main
#===========================================================
def main():
    argv = parse_args()
    print(pom_ver(argv.path))

#===========================================================
# Parse args
#===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Show Maven projec version.', 
        prog=const.PROG_TEMPLATE.format(MODULE_NAME)
    )
    parser.add_argument(
        '--path', 
        help='Path to root maven project directory'
    )
    return parser.parse_args()

#===========================================================
# Entry point
#===========================================================
if __name__ == '__main__':
    main()