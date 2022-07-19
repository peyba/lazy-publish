import argparse
import os

import const
import utils
import pom_dep
import colors
from classes import Waiter

MODULE_NAME = 'find-dependency'
PRINT_TEMPLATE = 'in ' + colors.CYAN + '{}' + colors.DEFAULT + ' version: ' + colors.YELLOW + '{}'  + colors.DEFAULT

def find_and_print_dep(path:str, art_id:str, group:str=None) -> str:
    i=0
    w = Waiter()
    for (dir_path, dir_names, file_names) in os.walk(path):
        for file in file_names:
            if (i % 100 == 0):
                w.print()
            if (file == const.POM_FILE):
                pom_file = utils.get_pom_path(dir_path)
                root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
                for art in pom_dep.dep_ver_list(root, ignore_error=True):
                    if (art.id == art_id and (group == None or art.group == group)):
                        print(PRINT_TEMPLATE.format(dir_path, art.version))
            i += 1

#===========================================================
# Main
#===========================================================
def main():
    argv = parse_args()
    find_and_print_dep(argv.path, argv.art_id, argv.group)

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
        default='.',
        help='Path to root maven project directory'
    )
    parser.add_argument(
        '--art-id', 
        required=True,
        help='Maven artifact id'
    )
    parser.add_argument(
        '--group', 
        required=False,
        help='Maven artifact group'
    )
    return parser.parse_args()

#===========================================================
# Entry point
#===========================================================
if __name__ == '__main__':
    main()