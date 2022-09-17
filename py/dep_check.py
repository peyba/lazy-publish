from classes import Artifact
from typing import List
import argparse
import logging

import utils
import colors
import pom_dep
import pom_ver
import const
import m2_installed

MODULE_NAME = 'check-dependency'
ART_TEMPLATE = '{:<30}{:<60}{}'
VERSION_TEMPLATE_COLOR = colors.RESET
VERSION_TEMPLATE = colors.paint('project:', VERSION_TEMPLATE_COLOR) + ' {:<22}' + colors.paint('sources:', VERSION_TEMPLATE_COLOR) + ' {:<22}' + colors.paint('m2:', VERSION_TEMPLATE_COLOR) + ' {}'


def get_current_art(art: Artifact) -> Artifact:
    art_pom = utils.path_join('..', art.id)
    current_ver = pom_ver.pom_ver(art_pom)
    current_art = Artifact()
    current_art.id = art.id
    current_art.group = art.group
    current_art.version = current_ver
    return current_art


# ===========================================================
# Return collored string created from Artifact
# - if dependency version is equal with artifact version, then green
# - if dependency version not equal with artifact version, then red
# - if artifact version or dependency version are unknown, then yellow 
# 
# params:
#   art - Artifact object (Artifact)
#   show_group - False: exclude groupId from result (bool)
# return:
#   collored string with groupId(optional), artifactId, version
# ===========================================================
def get_colored_art_for_print(art: Artifact, show_group: bool = True, no_color: bool = False) -> str:
    current_art = get_current_art(art)
    installed_versions = get_colored_m2_installed_for_print(art)

    if current_art.version is None:
        version = VERSION_TEMPLATE.format(colors.paint_yellow(art.version), colors.paint_yellow('Unknown'),
                                          installed_versions)
    elif current_art.version == art.version:
        version = VERSION_TEMPLATE.format(colors.paint_green(art.version), colors.paint_green(current_art.version),
                                          installed_versions)
    else:
        version = VERSION_TEMPLATE.format(colors.paint_red(art.version), colors.paint_green(current_art.version),
                                          installed_versions)

    if show_group:
        group = art.group + ' '
    else:
        group = ''

    return ART_TEMPLATE.format(group, colors.paint_cyan(art.id), version)


def get_colored_m2_installed_for_print(art: Artifact):
    installed_versions = m2_installed.m2_get_installed_versions(art)
    result = ''
    if art.version in installed_versions:
        for ver in installed_versions:
            if ver == art.version:
                result += '[' + colors.paint_yellow(ver) + ']'
            else:
                result += ver
            result += ', '
    else:
        for ver in installed_versions:
            result += ver + ', '
        result = colors.paint(result, colors.YELLOW_BG)

    result = utils.del_last_char(result, ',')
    return result


# ===========================================================
# TODO: description
# ===========================================================
def get_art_list_for_print(path: str, no_color: bool = False, short: bool = False) -> List[str]:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))

    arts = pom_dep.dep_ver_list(root)
    str_arts = []
    for art in arts:
        str_arts.append(get_colored_art_for_print(art, no_color=no_color))
    return str_arts


# ===========================================================
# Main
# ===========================================================
def main():
    argv = parse_args()
    logging.basicConfig(level=argv.log)
    for art in get_art_list_for_print(argv.path):
        print(art)


# ===========================================================
# Parse args
# ===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Check Maven projec dependensies.',
        prog=const.PROG_TEMPLATE.format(MODULE_NAME)
    )
    parser.add_argument(
        '--path',
        help='Path to root maven project directory'
    )
    parser.add_argument(
        '-s', '--short',
        required=False,
        action='store_true',
        help='Short interpretation'
    )
    parser.add_argument(
        '--no-color',
        required=False,
        action='store_true',
        help='Print uncolored result'
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
