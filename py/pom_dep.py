import xml.etree.ElementTree as et
import sys
import re
import argparse
import logging
from typing import List

import utils
import const
from classes import Artifact

MODULE_NAME = 'dependency'
DEP_PRINT_TEMPLATE = '{}.{}: {}'
MAX_DEP_VER_IN_DM_DEEP = 2
UNKNOWN = 'Unknown'


# ===========================================================
# Create list of Artifact objects for all project dependencies
# 
# params:
#   root - pom.xml root element (xml.etree.ElementTree.Element)
# return:
#   list of Artifact objects (classes.Artifact)
# ===========================================================
def dep_ver_list(root: et.Element, ignore_error: bool = False, exit_on_error: bool = False) -> List[Artifact]:
    dependencies = deps(root)
    l = []
    for d in dependencies:
        o = Artifact()
        o.id = dep_art(d)
        o.group = dep_group(d)
        o.version = dep_ver(root, d, ignore_error, exit_on_error)
        l.append(o)
    return l


# ===========================================================
# Return list of dependency elements
# 
# params:
#   root - pom.xml root element (xml.etree.ElementTree.Element)
# return:
#   list of dependency elements
#       (list[xml.etree.ElementTree.Element])
# ===========================================================
def deps(root: et.Element) -> List[et.Element]:
    dependencies = root.findall('./pom:dependencies/pom:dependency', namespaces=const.NAME_SPACE)
    return dependencies


# ===========================================================
# Return dependencyManagement element
# 
# params:
#   root - pom.xml root element (xml.etree.ElementTree.Element)
# return:
#   dependencyManagement element (xml.etree.ElementTree.Element)
# ===========================================================
def dm_deps(root: et.Element):
    return root.find('./pom:dependencyManagement', namespaces=const.NAME_SPACE)


# ===========================================================
# Search artifact in dependency elements list by artifact id
#
# params:
#   dependencies - list of dependency elements
#       (list[xml.etree.ElementTree.Element])
#   art_id - artifact id, from artifactId tag (str)
# return:
#   dependency element if found or None
#       (xml.etree.ElementTree.Element)
# ===========================================================
def dep(dependencies: List[et.Element], group: str, art_id: str):
    for d in dependencies:
        if group == dep_group(d):
            if d.findtext('./pom:artifactId', namespaces=const.NAME_SPACE) == art_id:
                return d
    return None


# ===========================================================
# Return artifactId tag text
# 
# params:
#   dep - dependency tag (xml.etree.ElementTree.Element)
# return:
#   artifactId tag text (str | None)
# ===========================================================
def dep_art(dep: et.Element):
    return dep.findtext('./pom:artifactId', namespaces=const.NAME_SPACE)


# ===========================================================
# Return groupId tag text
# 
# params:
#   dep - dependency tag (xml.etree.ElementTree.Element)
# return:
#   groupId tag text (str | None)
# ===========================================================
def dep_group(dep: et.Element):
    return dep.findtext('./pom:groupId', namespaces=const.NAME_SPACE)


# ===========================================================
# Return version tag text
# 
# params:
#   root - pom.xml root element (xml.etree.ElementTree.Element)
#   dep - dependency tag (xml.etree.ElementTree.Element)
# return:
#   version (str | None)
# ===========================================================
def dep_ver(root: et.Element, dep: et.Element, ignore_error: bool = False, exit_on_error: bool = False):
    ver = dep.findtext('./pom:version', namespaces=const.NAME_SPACE)
    if ver is None or ver == '':
        return dep_ver_in_dm(root, dep_group(dep), dep_art(dep), ignore_error, exit_on_error)
    elif ver == '${project.version}':
        return project_ver(root)
    elif ver[0] == '$':
        return dep_ver_by_prop(root, ver)
    else:
        return ver


# ===========================================================
#
# ===========================================================
def project_ver(root: et.Element) -> str:
    ver = root.findtext('./pom:version', namespaces=const.NAME_SPACE)
    return ver or parent_ver(root)


# ===========================================================
#
# ===========================================================
def parent_ver(root: et.Element) -> str:
    ver = root.findtext('./pom:parent/pom:version', namespaces=const.NAME_SPACE)
    return ver or UNKNOWN


# ===========================================================
#
# ===========================================================
def dep_ver_in_dm(root: et.Element, group: str, art_id: str, ignore_error: bool = False, exit_on_error: bool = False,
                  deep: int = 0):
    if deep > MAX_DEP_VER_IN_DM_DEEP:
        return UNKNOWN

    dm_list = root.findall('./pom:dependencyManagement/pom:dependencies/pom:dependency', const.NAME_SPACE)
    for dm in dm_list:
        dm_pom_root = get_dm_pom_root(root, dm, ignore_error, exit_on_error)
        if dm_pom_root is not None:
            dm_deps_var = dm_deps(dm_pom_root)
            if dm_deps_var is not None:
                deps_var = deps(dm_deps_var)
                if deps_var is not None:
                    dm_dep = dep(deps_var, group, art_id)
                    if dm_dep is not None:
                        return dep_ver(dm_pom_root, dm_dep)

            dep_dep_ver = dep_ver_in_dm(dm_pom_root, group, art_id, deep=deep + 1)
            if dep_dep_ver == UNKNOWN:
                continue
            else:
                return dep_dep_ver
    return UNKNOWN


# ===========================================================
#
# ===========================================================
def get_dm_pom_path(root: et.Element, dm: et.Element):
    m2 = utils.get_local_repository()
    group = utils.get_group_path(dep_group(dm))
    art = dep_art(dm)
    ver = dep_ver(root, dm)
    return utils.path_join(m2, group, art, ver, '{}-{}.pom'.format(art, ver))


# ===========================================================
#
# ===========================================================
def get_dm_pom_root(pom_root: et.Element, pom_dm: et.Element, ignore_error: bool, exit_on_error: bool):
    dm_pom_path = get_dm_pom_path(pom_root, pom_dm)
    if not utils.exists(dm_pom_path):
        if not ignore_error:
            if exit_on_error:
                sys.exit('Can\'t find ' + dm_pom_path)
            else:
                logging.debug('Can\'t find ' + dm_pom_path)
        return None
    return et.parse(dm_pom_path).getroot()


# ===========================================================
#
# ===========================================================
def dep_ver_by_prop(root: et.Element, ver_prop: str):
    prop_tag = re.search('[$][{](.+)[}]', ver_prop).group(1)
    prop_path = './pom:properties/pom:' + prop_tag
    ver = root.findtext(prop_path, namespaces=const.NAME_SPACE)
    if not ver:
        return UNKNOWN
    elif ver[0] == '$':
        return dep_ver_by_prop(root, ver)
    else:
        return ver


# ===========================================================
# RUN
# ===========================================================
def dep_list_for_print(path: str) -> List[str]:
    pom_file = utils.get_pom_path(path)

    root = utils.get_root(pom_file, show_error=(__name__ == '__main__'))

    arts = dep_ver_list(root)
    str_arts = []
    for art in arts:
        str_arts.append(DEP_PRINT_TEMPLATE.format(art.group, art.id, art.version))
    return str_arts


# ===========================================================
# Main
# ===========================================================
def main():
    argv = parse_args()
    logging.basicConfig(level=argv.log)
    for dep in dep_list_for_print(argv.path):
        print(dep)


# ===========================================================
# Parse args
# ===========================================================
def parse_args():
    parser = argparse.ArgumentParser(
        description='Show Maven project dependencies.',
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
