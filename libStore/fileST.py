#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

bdStore.py

Módulo librería para el acceso al systema de ficheros
en fileStore

"""

from hashlib import sha256
from os import lstat, path, readlink
import stat
import pwd
import grp
import subprocess
import magic
from libStore import configStore as cnf


class fst_stat():
    def __init__(self, filename):
        if not path.isfile(filename):
            self.exists = False
            return

        fstat = lstat(filename)

        self.userid = fstat.st_uid
        self.uname = pwd.getpwuid(fstat.st_uid).pw_name
        self.gid = fstat.st_gid
        self.gname = grp.getgrgid(fstat.st_gid).gr_name
        self.size = fstat.st_size
        self.rights = fstat.st_mode
        self.mode = stat.S_IMODE(self.rights)
        self.type = typeFile(self.rights)
        self.timeaccess = fstat.st_atime
        self.timemod = fstat.st_mtime
        self.timechang = fstat.st_ctime
        self.timecreat = 0
        mime = magic.Magic(mime=True)
        self.mime = mime.from_file(filename)
        self.chksum = hashFile(filename)
        if self.chksum is None:
            self.exists = False
        else:
            self.exists = True


def typeFile(mode):
    if stat.S_ISREG(mode):
        return 'f'
    elif stat.S_ISLNK(mode):
        return 'l'
    elif stat.S_IFDIR(mode):
        return 'd'
    else:
        return 'o'


def findFile(raiz, nombre):
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type f -iname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findDir(raiz, nombre):
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type d -iname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findLinkTo(raiz, nombre):
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type l -lname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findStored(chksum):
    filestored = findFile(cnf.conf['storePath'], chksum)
    return filestored


def findStoreLinks(origen):
    cmd = "find \"{}\" -type l -lname \"{}*\"".format(
        origen, cnf.conf["storePath"])
    links = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return links


def listStored():
    cmd = "find -P '{}' -type f -iname \"*\" -not -iname \".*\"".format(
        cnf.conf['storePath'])
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def hashFile(filename):
    if not path.isfile(filename):
        return None

    f = open(filename, 'rb')
    with f:
        return sha256(f.read()).hexdigest()


def getLinkTo(filename):
    if not path.islink(filename):
        return None
    return readlink(filename)
