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

def print_colored_art_ver(art:Artifact, show_group:bool):
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