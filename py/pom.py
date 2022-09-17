import xml.etree.ElementTree as et

import pom_dep
import const
from classes import Artifact


def get_ver(root: et.Element) -> str:
    if root:
        version = root.findtext('./pom:version', namespaces=const.NAME_SPACE)
        if version is not None:
            return version

    return None


def get_atr(root: et.Element):
    if root is not None:
        o = Artifact()
        o.id = pom_dep.dep_art(root)
        o.group = pom_dep.dep_group(root)
        o.version = pom_dep.dep_ver(root, root)
        return o

    return None
