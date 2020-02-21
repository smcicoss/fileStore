#! /usr/bin/python3

# -*- coding: utf-8 -*-
# ·

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
import tempfile
from libStore import configStore as cnf

# Variable global para almacenar la lista de ficheros de origen
listFOrigins = None  # ficheros
listLOrigins = None  # enlaces al Store


class sourceLinks():
    def __init__(self):
        self.listSources = tempfile.TemporaryFile(mode='w+t')

        for origin in cnf.conf["storedDirs"]:
            try:
                # Escribe tres líneas en el archivo temporal
                self.listSources.writelines(findStoreLinks(origin))
            finally:
                pass

            # break

    def __del__(self):
        self.listSources.close()

    def toBeggining(self):
        self.listSources.seek(0)


class fst_stat():
    # Mantiene los metadatos de un fichero
    def __init__(self, filename):
        # Obtiene los valores
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
    # Obtiene el tipo de fichero
    if stat.S_ISREG(mode):
        # Fichero regular
        return 'f'
    elif stat.S_ISLNK(mode):
        # Enlace simbólico
        return 'l'
    elif stat.S_IFDIR(mode):
        # Directorio
        return 'd'
    else:
        # Otros
        return 'o'


def findFile(raiz, nombre):
    # Busca un nombre de fichero en un arbol de directorios
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type f -iname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findDir(raiz, nombre):
    # Busca un nombre de directorio dentro de un arbol
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type d -iname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findLinkTo(raiz, nombre):
    # Busca un enlace simbolico que apunte a nombre dentro de un árbol
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type l -lname '{}'".format(start, nombre)
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def findStored(chksum):
    # Busca un fichero dentro del store
    filestored = findFile(cnf.conf['storePath'], chksum)
    return filestored


def findStoreLinks(origen):
    # Busca los enlaces simbílicos que apuntan al store dentro de un árbol
    cmd = "find \"{}\" -type l -lname \"{}*\"".format(
        origen, cnf.conf["storePath"])
    try:
        links = [line[0:]
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]
    except subprocess.CalledProcessError:
        links = None
    else:
        return links


def listStored():
    # Obtiene la lista de ficheros dentro del store
    cmd = "find -P '{}' -type f -iname \"*\" -not -iname \".*\"".format(
        cnf.conf['storePath'])
    paths = [line[0:]
             for line in subprocess.check_output(cmd, shell=True).splitlines()]
    return paths


def hashFile(filename):
    # Calcula el hash sha256 de un fichero
    if not path.isfile(filename):
        return None

    f = open(filename, 'rb')
    with f:
        return sha256(f.read()).hexdigest()


def getLinkTo(filename):
    # Obtiene el destino de un enlace simbólico
    if not path.islink(filename):
        return None
    return readlink(filename)
