import xml.etree.ElementTree as et
import sys
import re
from typing import List

import utils
from classes import Artifact
from const import NAME_SPACE

def dep_ver_list(root:et.Element) -> List[Artifact]:
    dependencies = deps(root)
    l = []
    for d in dependencies:
        o = Artifact()
        o.id = dep_art(d)
        o.group = dep_group(d)
        o.version = dep_ver(root, d)
        l.append(o)
    return l

def deps(root:et.Element):
    dependencies = root.findall('./pom:dependencies/pom:dependency', namespaces=NAME_SPACE)
    return dependencies

def dm_deps(root:et.Element):
    return root.find('./pom:dependencyManagement', namespaces=NAME_SPACE)

def dep(dependencies, art_id):
    for d in dependencies:
        if d.findtext('./pom:artifactId', namespaces=NAME_SPACE) == art_id:
            return d
    return None

def dep_art(dep:et.Element):
    return dep.findtext('./pom:artifactId', namespaces=NAME_SPACE)

def dep_group(dep:et.Element):
    return dep.findtext('./pom:groupId', namespaces=NAME_SPACE)

def dep_group(dep:et.Element):
    return dep.findtext('./pom:groupId', namespaces=NAME_SPACE)

def dep_group_path(group_is:str):
    path = ''
    for p in group_is.split('.'):
        path = utils.path_join(path, p)
    return path

def dep_ver(root:et.Element, dep:et.Element):
    ver = dep.findtext('./pom:version', namespaces=NAME_SPACE)
    if ver == None or ver == '':
        return dep_ver_in_dm(root, dep_art(dep))
    elif ver[0] == '$':
        return dep_ver_by_prop(root, dep)
    else:
        return ver

def dep_ver_in_dm(root:et.Element, art_id:str):
    dm_list = root.findall('./pom:dependencyManagement/pom:dependencies/pom:dependency', NAME_SPACE)
    for dm in dm_list:
        dm_pom_root = get_dm_pom_root(root, dm)
        dm_dep = dep(deps(dm_deps(dm_pom_root)), art_id)
        if dm_dep != None:
            return dep_ver(dm_pom_root, dm_dep)
    return 'Unknown'

def get_dm_pom_path(root:et.Element, dm:et.Element):
    m2 = utils.get_m2()
    group = dep_group_path(dep_group(dm))
    art = dep_art(dm)
    ver = dep_ver(root, dm)
    return utils.path_join(m2, 'repository', group, art, ver, '{}-{}.pom'.format(art, ver))

def get_dm_pom_root(pom_root:et.Element, pom_dm:et.Element):
    dm_pom_path = get_dm_pom_path(pom_root, pom_dm)
    if not utils.exists(dm_pom_path):
        sys.exit('Can\'t find ' + dm_pom_path)
    return et.parse(dm_pom_path).getroot()    

def dep_ver_by_prop(root:et.Element, dep:et.Element):
    prop = str(dep.findtext('./pom:version', namespaces=NAME_SPACE))
    prop_tag = re.search('[$][{](.+)[}]', prop).group(1)
    prop_path = './pom:properties/pom:' + prop_tag
    return root.findtext(prop_path, namespaces=NAME_SPACE)

