#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

bdStore.py

Módulo librería para el acceso a la base de datos de
fileStore

"""

import pymysql
import sys

from libStore import configStore as cnf
from libStore import constStore as cons


class bdStore(object):

    def __init__(self):
        # Establece conexión con el servidor de base de datos
        # Prepara un cursor y obtiene la versión
        # del gestor de BD
        self.__conect = pymysql.connect(
            cnf.conf["dbHost"], cnf.conf["dbUser"],
            cnf.conf["dbPasswd"], cnf.conf["baseDatos"])

        # prepara un objeto cursor usando el metodo cursor()
        self.cursor = self.__conect.cursor()

        # ejecuta el SQL query usando el metodo execute().
        self.cursor.execute("SELECT VERSION()")
        self.version = self.cursor.fetchone()

    def __del__(self):
        # desconecta del servidor
        self.cursor.close()
        self.__conect.close()

    def __get(self, sql):
        try:
            with self.__conect.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print("%sError SQL:\n\t%s%s" % (cons.MSG_ERROR, sql, cons.MSG_END))

        except Exception as err:
            code, mens = err.args
            print("{}Error {} en 'getFileId'\n\t{}{}".format(
                cons.MSG_ERROR, code, mens, cons.MSG_END))

        return None

    def __delete(self, tabla, id):
        sql = "DELETE FROM {} WHERE id = {};".format(tabla, id)

        try:
            with self.__conect.cursor() as cursor:
                cursor.execute(sql)
            self.__conect.commit()

        except Exception as error:
            print(error)
            return False

        else:
            return True

    def getFileId(self, chksum):
        # Obtiene el id del fichero en la BD
        sql = "SELECT id FROM files WHERE sha256sum LIKE '{}';".format(chksum)
        result = self.__get(sql)
        if result is not None:
            if len(result) > 0:
                return result[0][0]
        return None

    def getFileChk(self, id):
        # Obtiene el nombre del fichero en la BD
        sql = "SELECT sha256sum FROM files WHERE id = {}".format(id)
        result = self.__get(sql)
        if result is not None:
            if len(result) > 0:
                return result[0][0]
        return None

    def getListFiles(self):
        # obtiene la lista ordenada y completa de los ids de ficheros
        sql = "SELECT * FROM files ORDER BY id DESC;"
        result = self.__get(sql)
        if result is not None:
            if len(result) > 0:
                return result
            else:
                return []
        return None

    def getUrisOfFile(self, fileid):
        # Obtiene la lista de todos los orígenes del fichero
        sql = "SELECT id FROM uris WHERE file_id = {};".format(fileid)
        result = self.__get(sql)
        if result is not None:
            if len(result) > 0:
                return result
        return None

    def getUri(self, uriId):
        # Obtiene el path y el nombre de un origen
        sql = "SELECT path, filename FROM uris WHERE id = {}".format(uriId)
        result = self.__get(sql)
        if result is not None:
            if len(result) > 0:
                return result
        return None

    def insertFile(self, fileChk):
        # Inserta un fichero en la BD
        # Devuelve su id
        try:
            with self.__conect.cursor() as cursor:
                sql = "INSERT INTO files (sha256sum) VALUES ('%s');" % fileChk
                cursor.execute(sql)
            self.__conect.commit()

            with self.__conect.cursor() as cursor:
                cursor.execute("SELECT MAX(id) AS id FROM files;")
            return cursor.fetchone()[0]

        except pymysql.err.ProgrammingError:
            print("%sError SQL:\n\t%s%s" % (cons.MSG_ERROR, sql, cons.MSG_END))
            sys.exit(cons.ERROR_SQL)

        except Exception as err:
            code, mens = err.args
            print("{}Error {} en 'insertFile'\n\t{}{}".format(
                cons.MSG_ERROR, code, mens, cons.MSG_END))

        return None

    def delFile(self, fileid):
        return self.__delete('files', fileid)

    def getOrigen(self, storename):
        sql = "SELECT * FROM origenes WHERE storename = '{}';".format(
            storename)
        return self.__get(sql)

    def delUri(self, uriid):
        return self.__delete('uris', uriid)


BaseDatos = bdStore()
BDStore = BaseDatos
