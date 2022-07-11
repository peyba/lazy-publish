from typing import List
from os.path import exists
import sys
import argparse
import xml.etree.ElementTree as et

import const
import utils

PROG_TEMPLATE = '{} version'

def pom_ver(path:str):
    if path == None:
        pom_file = const.POM_FILE
    else:
        pom_file = utils.path_join(path, const.POM_FILE)

    if not exists(pom_file):
        if __name__ == '__main__':
            sys.exit('Can\'t find {}'.format(pom_file))
        else:
            return None
            
    root = et.parse(pom_file).getroot()
    return root.findtext('./pom:version', namespaces=const.NAME_SPACE)

def main():
    argv = parse_args()
    print(pom_ver(argv.path))

def parse_args():
    parser = argparse.ArgumentParser(
        description='Show Maven projec version.', 
        prog=PROG_TEMPLATE.format(const.APP_NAME)
    )
    parser.add_argument(
        '--path', 
        help='Path to root maven project directory'
    )
    return parser.parse_args()

if __name__ == '__main__':
    main()