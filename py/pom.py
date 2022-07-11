from os.path import exists
import xml.etree.ElementTree as et
import sys

import pom_dep
import const
import dep_check
from classes import Artifact


def main(args):
    if not exists(const.POM_FILE):
        sys.exit('Can\'t find pom.xml')

    root = et.parse(const.POM_FILE).getroot()

    for e in pom_dep.dep_ver_list(root):
        dep_check.print_colored_art_ver(e, True)

def ver(root:et.Element):
    return root.findtext('./pom:version', namespaces=const.NAME_SPACE)


if __name__ == '__main__':
    main(sys.argv)