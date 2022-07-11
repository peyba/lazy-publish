from tokenize import group
from classes import Artifact
import colors
import utils
import pom_ver

ART_TEMPLATE = "{:<30}{:<60}{}"
VERSION_TEMPLATE = "in use: {}; current: {}"

def get_current_art(art:Artifact) -> Artifact:
    art_pom = utils.path_join('..', art.id, 'pom.xml')
    current_ver = pom_ver.pom_ver(art_pom)
    current_art = Artifact()
    current_art.id = art.id
    current_art.group = art.group
    current_art.version = current_ver
    return current_art

def dep_colored_list_for_print(art:Artifact, show_group:bool) -> List[str]:
    current_art = get_current_art(art)
    if current_art.version == None:
        version = VERSION_TEMPLATE.format(colors.YELLOW + art.version + colors.RESET, colors.YELLOW + "Unknown" + colors.RESET)
    elif current_art.version == art.version:
        version = colors.GREEN + art.version + colors.RESET
    else:
        version = VERSION_TEMPLATE.format(colors.RED + art.version + colors.RESET, colors.GREEN + current_art.version + colors.RESET)
    
    if show_group:
        group = art.group + ' '
    else:
        group = ''
    
    print(ART_TEMPLATE.format(group, colors.CYAN + art.id + colors.RESET , version))

#===========================================================
# RUN
#===========================================================
def dep_list_for_print(path:str) -> List[str]:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))
    
    arts = dep_ver_list(root)
    str_arts = []
    for art in arts:
        str_arts.append(DEP_PRINT_TEMPLATE.format(art.group, art.id, art.version))
    return str_arts

#===========================================================
# Main
#===========================================================
def main():
    argv = parse_args()
    for dep in dep_list_for_print(argv.path):
        print(dep)

#===========================================================
# Parse args
#===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Show Maven projec dependensies.', 
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