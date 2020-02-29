#! /usr/bin/python3

# -*- coding: utf-8 -*-
# ·

u"""

fileST.py

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
from libStore import constStore as cons

# Variable global para almacenar la lista de ficheros de origen
listFOrigins = None  # ficheros
listLOrigins = None  # enlaces al Store


class Source():
    def __init__(self):
        self.listSources = tempfile.TemporaryFile(mode='w+t')

    def __del__(self):
        self.listSources.close()

    def __get(self):
        try:
            return self.listSources.readline().rstrip('\n').strip()
        except Exception as e:
            print(str(e))
            return None

    def __seek(self, pos):
        try:
            self.listSources.seek(pos)
            return True
        except Exception as err:
            print(str(err))
            return False

    def toBeggining(self):
        return self.__seek(0)

    def toLine(self, nline):
        return self.__seek(nline)

    def getLen(self):
        point = self.listSources.tell()
        if not self.__seek(0):
            return None
        try:
            return len(self.listSources.readlines())
        except Exception as err:
            print(str(err))
            return None
        finally:
            self.__seek(point)

    def getLine(self, pos):
        if not self.__seek(pos):
            return None
        return self.__get()

    def getFirst(self):
        if not self.__seek(0):
            return None
        return self.__get()

    def getNext(self):
        return self.__get()

    def search(self, fullname):
        if not self.__seek(0):
            return None

        for f in self.listSources:
            if f == fullname:
                return True
        return False


class sourceLinks(Source):
    def __init__(self):
        super().__init__()

        for origin in cnf.conf["storedDirs"]:
            print("Recopilando enlaces en {}".format(origin))
            try:
                # Escribe líneas en el archivo temporal
                links = findStoreLinks(origin)
                if links is not None:
                    if len(links) > 0:
                        self.listSources.writelines(findStoreLinks(origin))
            except Exception as err:
                print("Error al grabar fichero temporal de ficheros origen")
                print(str(err))
                print("Termino")
                exit(cons.ERROR_FILE)


class sourceFiles(Source):
    def __init__(self):
        super().__init__()

        for origin in cnf.conf["storedDirs"]:
            print("Recopilando ficheros en {}".format(origin))
            try:
                # Escribe tres líneas en el archivo temporal
                self.listSources.writelines(findFile(origin, "*"))
            except Exception as err:
                print("Error al grabar fichero temporal de ficheros origen")
                print(str(err))
                print("Termino")
                exit(cons.ERROR_FILE)


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
        return []

    start = path.abspath(raiz)

    cmd = "find -P \"%s\" -type f -iname \"%s\" -not -name \".*\"" % (
        start, nombre)
    cmd += " -exec realpath \"{}\" \\; 2>/dev/null"

    try:
        paths = [line[0:].decode("utf-8") + "\n"
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]

    except subprocess.CalledProcessError:
        return None

    else:
        return paths


def findDir(raiz, nombre):
    # Busca un nombre de directorio dentro de un arbol
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type d -iname '{}' 2>/dev/null".format(start, nombre)
    try:
        paths = [line[0:].decode('utf-8')
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]

    except subprocess.CalledProcessError:
        return None

    else:
        return paths


def findLinkTo(raiz, nombre):
    # Busca un enlace simbolico que apunte a nombre dentro de un árbol
    if not path.isdir(raiz):
        return None

    start = path.abspath(raiz)

    cmd = "find -P '{}' -type l -lname '{}' 2>/dev/null".format(start, nombre)
    try:
        paths = [line[0:].decode("utf-8")
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]

    except subprocess.CalledProcessError as subperr:
        if subperr.returncode == 1:
            paths = [line[0:].decode('utf-8')
                     for line in subperr.output.splitlines()]
        else:
            exit(cons.ERROR_FIND)

    return paths


def findStored(chksum):
    # Busca un fichero dentro del store
    return findFile(cnf.conf['storePath'], chksum)


def findStoreLinks(origen):
    # Busca los enlaces simbólicos que apuntan al 'Store' dentro de un árbol
    cmd = "find \"{}\" -type l -lname \"{}*\" 2>/dev/null".format(
        origen, cnf.conf["storePath"])
    try:
        links = [line[0:].decode('utf-8') + "\n"
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]

    except subprocess.CalledProcessError:
        links = None

    else:
        return links


def listStored():
    # Obtiene la lista de ficheros dentro del store
    cmd = "find -P '{}' -type f -iname \"*\" -not -iname \".*\"".format(
        cnf.conf['storePath'])

    try:
        paths = [line[0:].decode('utf-8')
                 for line in subprocess.check_output(cmd, shell=True).splitlines()]

    except subprocess.CalledProcessError:
        return None

    else:
        return paths


def hashFile(filename):
    # Calcula el hash sha256 de un fichero
    if not path.isfile(filename):
        return None

    f = open(filename, 'rb')
    with f:
        return sha256(f.read()).hexdigest()


def getTargetLink(filename):
    # Obtiene el destino de un enlace simbólico
    if not path.islink(filename):
        return None
    return readlink(filename)


def fileExists(filename):
    if path.isfile(filename):
        return True
    else:
        return False
