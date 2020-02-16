#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

bdStore.py

Módulo librería para el acceso al systema de ficheros
en fileStore

"""

from hashlib import sha256
from os import lstat, path
import pwd
import grp
import subprocess
# from libStore import constStore as cons
from libStore import configStore as cnf

claves_st = ["st_mode", "st_dev", "st_nlink", "st_uid",
             "st_gid", "st_size", "st_atime", "st_mtime", "st_ctime"]


class fst_stat():
    def __init__(self, result):
        for clave in claves_st:
            self[clave] = result[clave]
        self.st_uname = pwd.getpwuid(result.st_uid).pw_name
        self.st_gname = grp.getgrgid(result.st_gid).gr_name


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


def hashFile(filename):
    if not path.isfile(filename):
        return None

    f = open(filename, 'rb')
    with f:
        return sha256(f.read()).hexdigest()


def getFileStat(filename):
    if not path.isfile(filename):
        return None

    fstat = lstat(filename)

    return fst_stat(fstat)
