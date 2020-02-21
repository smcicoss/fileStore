#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

prueba.py

Módulo librería para el acceso a la base de datos de
fileStore

"""
# TODO: crear sistema de registro

import time
import sys
from os import path, remove
from libStore import constStore as cons
from libStore import configStore as cnf
from libStore.bdStore import BaseDatos as BDStore
from libStore import fileST

days = ['Domingo', 'Lunes', 'Martes',
        'Miercoles', 'Jueves', 'Viernes', 'Sabado']


def presenta():
    print(cons.MSG_OK + "\ncheckStore." + cons.MSG_END)
    print("------------------------------------------------")
    print("Gestor Base de Datos: %s%s%s" %
          (cons.MSG_OK, BDStore.version[0], cons.MSG_END))
    print("Path al almacén: %s%s%s" %
          (cons.MSG_OK, cnf.conf["storePath"], cons.MSG_END))
    print(days[int(time.strftime("%w"))] + time.strftime(" %d/%m/%Y %H:%M:%S"))
    print("------------------------------------------------\n")

# TODO:
#       obtener listado de origen sobre fichero temporal

##########################################################################


def scanStoreInDB():
    # escaneo el store en busca de ficheros sin registro
    print("\nObteniendo la lista de ficheros")
    lista = fileST.listStored()
    for entry in lista:
        fstored = entry.decode('utf-8')
        namestored = path.basename(fstored)
        fsid = BDStore.getFileId(namestored)
        if fsid is None:
            print("{}{} no se encuentra en la base de datos{}".format(
                cons.MSG_ERROR, namestored, cons.MSG_END))
            # TODO: registrar caso
            # --------------------------------------------------------

            # 1º - Buscar enlace que apunte a
            linksOrigin = []
            for origin in cnf.conf["storedDirs"]:
                linksOrigin.append(fileST.findLinkTo(origin, fstored))
            if len(linksOrigin) > 0:
                # si existe
                # 2º - registrar fichero
                new_id = BDStore.insertFile(namestored)
                if new_id is None:
                    print("%sError al insertar %s\n%sTermino%s" % (
                        cons.MSG_ERROR, namestored, cons.MSG_ALERT, cons.MSG_END))
                    sys.exit(cons.ERROR_DB)
            # TODO:
            #       3º - obtener metadatos y registrarlos
            #   si no existe
            #       2º - buscar origen mismo contenido
            #       si existe
            #           3º - registrar fichero
            #           4º - registrar metadatos
            #           5º - borrar origen
            #           6º - crear enlace
            #       si no existe
            #           3º - registrar fichero
            #           4º - registrar huérfano
        else:
            print("\n{} -> {}".format(fstored, fsid))

    print("\n\n---------------------------------\n\n")


##########################################################################
def scanLinksOrigins():
    # busco enlaces al store en origen

    origenes = cnf.conf["storedDirs"]
    for origen in origenes:
        enlaces = fileST.findStoreLinks(origen)
        print("Existen {:6} enlaces en {}".format(len(enlaces), origen))
        if len(enlaces) > 0:
            for enlace in enlaces:
                print("\n%s" % enlace.decode('utf-8'))
                linkTo = fileST.getLinkTo(enlace).decode('utf-8')
                print("\tapunta a: %s" % linkTo)
                if path.isfile(linkTo):
                    # OK - nada que hacer
                    pass
                else:
                    real = fileST.findStored(path.basename(linkTo))
                    if len(real) > 0:
                        print("\t%spero el fichero se encuentra en %s%s" %
                              (cons.MSG_WARNING, real[0], cons.MSG_END))
                        # TODO: Corregir
                    else:
                        print("\t%spero el destino no existe%s" %
                              (cons.MSG_ERROR, cons.MSG_END))
                        remove(enlace)


##########################################################################
def checkDB():
    # escaneo la base de datos en busca de errores de registro
    # Lista completa de ids de ficheros
    listFiles = BDStore.getListFiles()
    print("Total registros a procesar: {}".format(len(listFiles)))

    # Por cada Fichero
    for regf in listFiles:
        fileID = regf[0]
        fileChk = regf[1]

        # path completo del fichero almacenado
        fileStored = fileST.findStored(fileChk)[0].decode("utf-8")
        print("\nStored[%i]: %s" % (fileID, fileStored))

        # obtiene el id de los origenes del fichero
        uris = BDStore.getUrisOfFile(fileID)
        if len(uris) < 1:
            # el fichero no tiene uri almacenada
            # TODO: registrar caso
            #       buscar solución
            print("{}{} no tiene uri asociada en BD{}".format(
                cons.MSG_ERROR, fileChk, cons.MSG_END))
            sys.exit(3)

        for regu in uris:
            # por cada id de origen
            uriID = regu[0]
            # obtiene el origen
            pathUri, nameUri = BDStore.getUri(uriID)[0]
            fileURI = path.join(pathUri, nameUri)
            print("\tURI: %s" % fileURI)
            # obtiene los datos del origen
            pathFileUri = fileST.fst_stat(fileURI)
            if not pathFileUri.exists:
                print("\t\t%sNo existe%s" % (cons.MSG_ERROR, cons.MSG_END))
                # TODO: generar el enlace
            elif pathFileUri.type == 'l':
                # es un enlace
                flinkto = fileST.getLinkTo(fileURI)
                if fileStored == flinkto:
                    # Estado correcto
                    print("\t\t%sExiste y es %s apuntando a :%s" %
                          (cons.MSG_OK, pathFileUri.mime, cons.MSG_END))
                    print("\t\t %s%s%s" %
                          (cons.MSG_OK, flinkto, cons.MSG_END))
                else:
                    # enlace apuntando a otro fichero
                    # TODO: registrar el caso
                    #       buscar solución
                    print("\t\t%sExiste y es %s apuntando a :%s" %
                          (cons.MSG_ERROR, pathFileUri.mime, cons.MSG_END))
                    print("\t\t %s%s%s" %
                          (cons.MSG_ERROR, flinkto, cons.MSG_END))
            elif pathFileUri.type == 'o':
                # no es un fichero ni un enlace
                # TODO: registrar el caso
                #           buscar solución
                print("\t\t%sExiste y es %s %s" %
                      (cons.MSG_WARNING, pathFileUri.mime, cons.MSG_END))
            elif fileChk != pathFileUri.chksum:
                # Es un fichero con contenido diferente
                # TODO: Registrar el caso
                #           buscar solución
                print("\t\t%sExiste y es %s %s" %
                      (cons.MSG_ERROR, pathFileUri.mime, cons.MSG_END))
                print("\t\t%sPero ha cambiado su contenido%s" %
                      (cons.MSG_ERROR, cons.MSG_END))
            else:
                print("\t\t%sExiste el origen y es %s %s" %
                      (cons.MSG_WARNING, pathFileUri.mime, cons.MSG_END))
                # TODO: registrar el caso
                #           buscar solución


presenta()

# scanStoreInDB()
# scanLinksOrigins()

print("Escaneando origen en busca de enlaces")
linksOrigins = fileST.sourceLinks()
linksOrigins.toBeggining()

print("Total encontrados: {}".format(len(linksOrigins.listSources)))
for linea in linksOrigins.listSources:
    print(linea.rstrip())
