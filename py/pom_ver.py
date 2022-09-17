import argparse
import logging

import const
import utils
import pom

MODULE_NAME = 'version'


# ===========================================================
# Return Maven app version (pom.xml/project/version)
# If parameter path is None or empty method use current 
# directory for search pom.xml
#
# params:
#   path - Path to the root Maven project directory (str)
# return:
#   version (str)
# ===========================================================
def pom_ver(path: str) -> str:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
    return pom.get_ver(root)


# ===========================================================
# Main
# ===========================================================
def main():
    argv = parse_args()
    logging.basicConfig(level=argv.log)
    print(pom_ver(argv.path))


# ===========================================================
# Parse args
# ===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Show Maven projec version.',
        prog=const.PROG_TEMPLATE.format(MODULE_NAME)
    )
    parser.add_argument(
        '--path',
        help='Path to root maven project directory'
    )
    parser.add_argument(
        '--log',
        choices=logging._nameToLevel,
        help='Log level'
    )
    return parser.parse_args()


# ===========================================================
# Entry point
# ===========================================================
if __name__ == '__main__':
    main()
