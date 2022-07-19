from classes import Artifact
from typing import List
import argparse

import utils
import colors
import pom_dep
import pom_ver
import const

MODULE_NAME = 'check-dependency'
ART_TEMPLATE = '{:<30}{:<60}{}'
VERSION_TEMPLATE = 'in use: {}; current: {}'

def get_current_art(art:Artifact) -> Artifact:
    art_pom = utils.path_join('..', art.id)
    current_ver = pom_ver.pom_ver(art_pom)
    current_art = Artifact()
    current_art.id = art.id
    current_art.group = art.group
    current_art.version = current_ver
    return current_art

#===========================================================
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
#===========================================================
def get_colored_art_for_print(art:Artifact, show_group:bool=True) -> str:
    current_art = get_current_art(art)
    if current_art.version == None:
        version = VERSION_TEMPLATE.format(colors.YELLOW + art.version + colors.RESET, colors.YELLOW + 'Unknown' + colors.RESET)
    elif current_art.version == art.version:
        version = colors.GREEN + art.version + colors.RESET
    else:
        version = VERSION_TEMPLATE.format(colors.RED + art.version + colors.RESET, colors.GREEN + current_art.version + colors.RESET)
    
    if show_group:
        group = art.group + ' '
    else:
        group = ''
    
    return ART_TEMPLATE.format(group, colors.CYAN + art.id + colors.RESET , version)

#===========================================================
# TODO: discription
#===========================================================
def get_art_list_for_print(path:str) -> List[str]:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
    
    arts = pom_dep.dep_ver_list(root)
    str_arts = []
    for art in arts:
        str_arts.append(get_colored_art_for_print(art))
    return str_arts

#===========================================================
# Main
#===========================================================
def main():
    argv = parse_args()
    for art in get_art_list_for_print(argv.path):
        print(art)

#===========================================================
# Parse args
#===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Check Maven projec dependensies.', 
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