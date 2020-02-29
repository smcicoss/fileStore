#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

prueba.py

Módulo librería para el acceso a la base de datos de
fileStore

"""

from os import path
# from stat import *
from libStore import constStore as cons
from libStore import configStore as cnf
from libStore.bdStore import BDStore
from libStore import fileST

if __name__ == '__main__':
    print(cons.MSG_OK + "\nScript de pruebas de fileStore." + cons.MSG_END)
    print("------------------------------------------------")
#    db = bdStore.BaseDatos
    print("Gestor Base de Datos: %s%s%s" %
          (cons.MSG_OK, BDStore.version[0], cons.MSG_END))
    print("Path al almacén: %s%s%s" %
          (cons.MSG_OK, cnf.conf["storePath"], cons.MSG_END))
    print("------------------------------------------------\n")

    # chksum del file id = 1 en bd
    chksum = "0a4a27ae3c098749df9ded52b0a56f8a8484f10055eec69fa891aefe5644a72a"
    fid = BDStore.getFileId(chksum)
    print("file id: {}".format(fid))

    # utilizamos la función getFileChk()
    chksum = BDStore.getFileChk(fid)

    # busca el fichero en el Store
    result = fileST.findStored(chksum)
    dest = None
    if result is not None:
        if len(result) > 0:
            dest = result[0]

    print("El fichero en el almacen es:\n\t{}".format(dest))

    enlace = fileST.findLinkTo("/home/simo/Datos/MyBook/almacen", dest)

    if len(enlace) == 0:
        print("%sEl fichero\n\t'%s'\nno tiene enlace en\n\t%s%s" %
              (cons.MSG_WARNING, chksum, "/home/simo/Datos/MyBook/almacen", cons.MSG_END))
    else:
        print("\n{} - Fichero en el almacén:\n\t{}".format(len(enlace), enlace))

    uris = BDStore.getUrisOfFile(fid)
    for u in uris:
        print("")
        reg = BDStore.getUri(u[0])
        upath = reg[0][0]
        uname = reg[0][1]
        ufullname = "{}/{}".format(upath, uname)
        print(ufullname)
        if path.exists(ufullname):
            print("El fichero existe en\n\t{}".format(ufullname))
            if fileST.hashFile(ufullname) == chksum:
                print("\ty no ha sido modificado")
            else:
                print("\tpero ha sido modificado")
            fstat = fileST.fst_stat(ufullname)
            print("propietario: %s" % fstat.uname)
            print("rights: {} - {}".format(fstat.rights, oct(fstat.rights)))
            print("modo: {}\ttipo: {}".format(
                "%o" % fstat.mode, fstat.type))
        else:
            print("El fichero no existe en el path registrado")

    # enlaces = fileST.findStoreLinks(cnf.conf["storedDirs"][10])
    print("\nObteniendo la lista de enlaces en origen")
    enlaces = fileST.sourceLinks()
    if enlaces.listSources is not None:
        if enlaces.getLen() > 0:
            print(cons.MSG_ALERT, enlaces.getFirst(), cons.MSG_END)
            print(cons.MSG_ALERT, enlaces.listSources, cons.MSG_END)

    # enlaces = fileST.findStoreLinks(cnf.conf["storedDirs"][10])
    print("\nObteniendo la lista de ficheros en origen")
    ficheros = fileST.sourceFiles()
    if ficheros.listSources is not None:
        lenFicheros = ficheros.getLen()
        if lenFicheros > 0:
            print("%sEncontrados %s ficheros en origen%s" %
                  (cons.MSG_ALERT, lenFicheros, cons.MSG_END))
            print("%sPrimer Fichero: %s%s" %
                  (cons.MSG_ALERT, ficheros.getFirst(), cons.MSG_END))
            print("%sSiguiente Fichero: %s%s" %
                  (cons.MSG_ALERT, ficheros.getNext(), cons.MSG_END))
