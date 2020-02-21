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

    # busca el fichero en el Store
    dest = fileST.findStored(chksum)[0].decode('utf-8')
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
            print("El fichero existe en {}".format(ufullname))
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

    enlaces = fileST.findStoreLinks(cnf.conf["storedDirs"][2])
    if enlaces is not None:
        print(cons.MSG_ALERT, enlaces[0].decode("utf-8"), cons.MSG_END)
        print(cons.MSG_ALERT, len(enlaces), cons.MSG_END)

    print(BDStore.insertFile("pepe botella"))
