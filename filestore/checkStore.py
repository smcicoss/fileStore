#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""
prueba.py.
Módulo librería para el acceso a la base de datos de
fileStore.
"""
# TODO: crear sistema de registro

import time
import sys
from os import path, remove
from libStore import constStore as cons
from libStore import configStore as cnf
from libStore.bdStore import BDStore
from libStore import fileST

days = ['Domingo', 'Lunes', 'Martes',
        'Miercoles', 'Jueves', 'Viernes', 'Sabado']


##########################################################################
# presentación inicial
def presenta():
    print("\n%s%s%s" % (cons.MSG_OK, '#' * 80, cons.MSG_END))
    print(cons.MSG_OK + "checkStore." + cons.MSG_END)
    print("%s\n" % ("-" * 80))
    print("Gestor Base de Datos: %s%s%s" %
          (cons.MSG_OK, BDStore.version[0], cons.MSG_END))
    print("Path al almacén: %s%s%s" %
          (cons.MSG_OK, cnf.conf["storePath"], cons.MSG_END))
    print(days[int(time.strftime("%w"))] + time.strftime(" %d/%m/%Y %H:%M:%S"))
    print("%s\n" % ("-" * 80))


##########################################################################
# escaneo el Store en busca de ficheros sin registro
def scanStoredInDB():
    print("%s\n%sComprobando la inclusión de los ficheros de el 'Store' en la 'DB'%s\n%s" % (
        '-' * 80, cons.MSG_WARNING, cons.MSG_END, '-' * 80))
    print("Obteniendo la lista de ficheros en el 'Store'")

    lista = fileST.listStored()
    print("Ficheros encontrados: %s" % len(lista))
    print("Comprobando inclusión en BD")
    n = 0
    print("{0:7} - {1:64} - {2:7}".format("número", "nombre", "id"))
    for fstored in lista:
        namestored = path.basename(fstored)
        fsid = BDStore.getFileId(namestored)
        n += 1
        if fsid is None:
            pfsid = ""
        else:
            pfsid = fsid
        print("{0:7} - {1:64} - {2:7}".format(n, namestored, pfsid), end="\r")
        if fsid is None:
            print("\n{}{}\n\tno se encuentra en la base de datos{}".format(
                cons.MSG_ERROR, namestored, cons.MSG_END))
            # Incluyo en DB
            new_id = BDStore.insertFile(namestored)
            if new_id is None:
                print("%sError al insertar %s\n%sTermino%s" % (
                    cons.MSG_ERROR, namestored, cons.MSG_ALERT, cons.MSG_END))
                sys.exit(cons.ERROR_DB)
            else:
                print("Insertado con el id: {}".format(new_id))

    if len(lista) == n:
        print("\n{}De los {} ficheros en el 'Store' están registrados {}{}\n".format(
            cons.MSG_OK, len(lista), n, cons.MSG_END))
    else:
        print("\n{}De los {} ficheros en el 'Store' están registrados {}{}\n".format(
            cons.MSG_WARNING, len(lista), n, cons.MSG_END))


##########################################################################
# escaneo la DB en busca de registros huérfanos
def scanDBInStore():
    print("%s\n%sComprobando la existencia de los ficheros registrados en la 'DB'%s\n%s" % (
        '-' * 80, cons.MSG_WARNING, cons.MSG_END, '-' * 80))
    print("Obteniendo la lista de ficheros en la 'DB'")

    listfdb = BDStore.getListFiles()
    if listfdb is None:
        print("%sError al obtener la lista%s" %
              (cons.MSG_ERROR, cons.MSG_END))
        return False

    print("Existen {:,.0f} ficheros en la DBStore".format(
        len(listfdb)).replace(',', '.'))
    listfst = fileST.listStored()
    print("y en el 'Store' {:,.0f}".format(len(listfst)).replace(',', '.'))

    n = 0
    for fdb in listfdb:
        if not any(fdb[1] in fullpath for fullpath in listfst):
            print("\nEl fichero {}\n\tno existe en el 'Store'".format(fdb[1]))
            iduris = BDStore.getUrisOfFile(fdb[0])
            if iduris is None or len(iduris) == 0:
                print("\tNo existen datos registrados del origen")
                continue
        else:
            n += 1
            print(fdb, end='\r')

    if len(listfdb) == n:
        print("\n{}De los {} ficheros en el 'Store' están registrados {}{}\n".format(
            cons.MSG_OK, len(listfdb), n, cons.MSG_END))
    else:
        print("\n{}De los {} ficheros en el 'Store' están registrados {}{}\n".format(
            cons.MSG_WARNING, len(listf), n, cons.MSG_END))


##########################################################################
# escaneo y compruebo enlaces al 'Store' en origen
def scanLinksOrigins():
    print("%s\n%sComprobando la existencia de enlaces al 'Store' en el 'origen'%s\n%s" % (
        '-' * 80, cons.MSG_WARNING, cons.MSG_END, '-' * 80))
    print("Obteniendo la lista de enlaces en 'origen'")

    links = fileST.sourceLinks()
    print("Existen {} enlaces".format(links.getLen()))

    links.toBeggining()
    nok = 0
    borrados = 0
    reubicados = 0
    for element in links.listSources:
        # acondiciono la cadena
        linkname = element.rstrip('\n').strip()

        # obtengo el destino del enlace
        linkto = fileST.getTargetLink(linkname)

        if not fileST.fileExists(linkto):
            print("El fichero\n\t%s\napunta a:\n\t%s\n y este no existe." %
                  (linkname, linkto))

            # compruebo si está reubicado
            storedname = path.basename(linkto)
            storedfullpath = fileST.findStored(storedname)
            if storedfullpath is None or len(storedfullpath) == 0:
                # enlace inútil, borro
                print("Enlace perdido.\n\t%sBorro%s" %
                      (cons.MSG_ERROR, cons.MSG_END))
                remove(linkname)
                borrados += 1
            else:
                print("Existe un fichero en {}".format(storedfullpath))
                reubicados += 1
                # TODO: Corregir el enlace.
        else:
            nok += 1

    print("\n{} enlaces correctos\n{} borrados\n{} reubicados\n".format(
        nok, borrados, reubicados))


##########################################################################
# escaneo y compruebo ficheros en origen
def scanFilesOrigin():
    print("%s\n%sComprobando la existencia de ficheros en el 'origen'%s\n%s" % (
        '-' * 80, cons.MSG_WARNING, cons.MSG_END, '-' * 80))
    print("Obteniendo la lista de enlaficheros en 'origen'")

    files = fileST.sourceFiles()
    print("Existen {:,.0f} ficheros en origen".format(
        files.getLen()).replace(',', '.'))

    files.toBeggining()

    nok = 0
    repe = 0
    borrados = 0
    for fo in files.listSources:
        # acondiciono
        forigen = fo.rstrip('\n').strip()

        # obtengo metadatos
        fostat = fileST.fst_stat(forigen)

        # checksum sha256 -> storename
        storename = fostat.chksum

        # busco ese nombre en el Store
        storefullname = fileST.findStored(storename)
        if storefullname is not None and len(storefullname) > 0:
            # el fichero esta en el Store y en origen
            storefullname = storefullname[0].rstrip('\n').strip()
            repe += 1
        else:
            # correcto, no está en el store
            nok += 1
            print("{}{:,.0f} - {}{}".format(cons.MSG_OK, nok, storename,
                                            cons.MSG_END).replace(',', '.'), end='\r')
            continue

        idstoredfile = BDStore.getFileId(storename)
        if idstoredfile is None:
            print("{}El fichero {} en el 'Store' no está en la 'DB'{}".format(
                cons.MSG_ERROR, storename, cons.MSG_END))
            exit(cons.ERROR_INTERNAL)

        # el fichero existe en la DB
        dborigenes = BDStore.getOrigen(storename)
        if dborigenes is None or len(dborigenes) == 0:
            # No hay datos de origen. Borro fichero y registro
            BDStore.delFile(idstoredfile)
            remove(storefullname)
            borrados += 1
            print("{}{:,.0f} - {}{}".format(cons.MSG_ALERT, borrados,
                                            storename,
                                            cons.MSG_END).replace(
                                                ',', '.'), end='\r')
        else:
            for dborigen in dborigenes:
                dbfullpath = path.join(dborigen[3], dborigen[4])
                if forigen == dbfullpath:
                    print("el fichero existe en origen y en 'Store'")
                    # borrar uri en db
                    if BDStore.delUri(dborigen[1]):
                        print("\n{}{:,.0f} - {}{}".format(cons.MSG_ALERT, borrados,
                                                          forigen,
                                                          cons.MSG_END).replace(
                            ',', '.'), end='\r')
                    break
            borrados += 1
            print("{}{:,.0f} - {}{}".format(cons.MSG_ALERT, borrados,
                                            storename,
                                            cons.MSG_END).replace(
                                                ',', '.'), end='\r')

    print("\n{} ficheros correctos\n{} repetidos\n{} borrados\n".format(
        nok, repe, borrados))


##########################################################################
# escaneo la base de datos en busca de errores de registro
def checkDB():
    # TODO
    pass


presenta()

scanStoredInDB()
scanDBInStore()
scanLinksOrigins()
scanFilesOrigin()
print()
