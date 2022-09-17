import argparse
from typing import List
import os
import logging

import const
import utils
import pom
from classes import Artifact

MODULE_NAME = 'm2-installed'
JAR_EXTENSION = '.jar'
POM_EXTENSION = '.pom'
SOURCE_FILE_NAME_PART = '-sources'


def m2_installed(path: str) -> List[str]:
    pom_file = utils.get_pom_path(path)
    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
    art = pom.get_atr(root)
    return m2_get_installed_versions(art)


def m2_get_installed_versions(art: Artifact) -> List[str]:
    m2_rep = utils.get_local_repository()
    group = utils.get_group_path(art.group)
    art_m2_path = utils.path_join(m2_rep, group, art.id)
    if not utils.exists(art_m2_path):
        return []
    v = []
    for (dir_path, dir_names, file_names) in os.walk(art_m2_path):
        if (dir_path == art_m2_path): continue

        for full_file_name in file_names:
            file_name, file_extension = os.path.splitext(full_file_name)
            if file_extension == JAR_EXTENSION or file_extension == POM_EXTENSION:
                if file_name.find(SOURCE_FILE_NAME_PART) == -1:
                    ver = m2_get_version_from_jar(file_name, art.id)
                    if not ver == None:
                        v.append(ver)
                        break
    return sorted(v)


def m2_get_version_from_jar(jar_name: str, art_id: str) -> str:
    if art_id in jar_name:
        return jar_name.replace(art_id + '-', '')
    return None


# ===========================================================
# Main
# ===========================================================
def main():
    argv = parse_args()
    logging.basicConfig(level=argv.log)
    versions = m2_installed(argv.path)
    for ver in versions:
        print(ver)


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
