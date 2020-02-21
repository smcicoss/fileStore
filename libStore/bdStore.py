#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

bdStore.py

Módulo librería para el acceso a la base de datos de
fileStore

"""

import pymysql

from libStore import configStore as cnf


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

    def getFileId(self, chksum):
        # Obtiene el id del fichero en la BD
        sql = "SELECT id FROM files WHERE sha256sum LIKE '{}'".format(chksum)
        self.cursor.execute(sql)
        id = self.cursor.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    def getFileChk(self, id):
        # Obtiene el nombre del fichero en la BD
        sql = "SELECT sha256sum FROM files WHERE id = {}".format(id)
        self.cursor.execute(sql)
        chk = self.cursor.fetchone()
        return chk[0]

    def getListFiles(self):
        # obtiene la lista ordenada y completa de los ids de ficheros
        sql = "SELECT * FROM files ORDER BY id;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getUrisOfFile(self, fileid):
        # Obtiene la lista de todos los orígenes del fichero
        sql = "SELECT id FROM uris WHERE file_id = {}".format(fileid)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getUri(self, uriId):
        # Obtiene el path y el nombre de un origen
        sql = "SELECT path, filename FROM uris WHERE id = {}".format(uriId)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insertFile(self, fileChk):
        # Inserta un fichero en la BD
        # Devuelve su id
        try:
            with self.__conect.cursor() as cursor:
                sql = "INSERT INTO files (sha256sum) VALUES ('%s');" % fileChk
                cursor.execute(sql)
            self.__conect.commit()

            with self.__conect.cursor() as cursor:
                self.cursor.execute("SELECT MAX(id) AS id FROM files;")
            return self.cursor.fetchone()[0]

        except pymysql.err.DataError:
            return None
        except pymysql.err.IntegrityError:
            return None


BaseDatos = bdStore()
BDStore = BaseDatos
