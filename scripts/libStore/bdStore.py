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
        # Establece conexión con base de datos
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
        sql = "SELECT id FROM files WHERE sha256sum LIKE '{}'".format(chksum)
        self.cursor.execute(sql)
        id = self.cursor.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    def getFileChk(self, id):
        sql = "SELECT sha256sum FROM files WHERE id = {}".format(id)
        self.cursor.execute(sql)
        chk = self.cursor.fetchone()
        return chk[0]

    def getListFiles(self):
        sql = "SELECT * FROM files ORDER BY id;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getUrisOfFile(self, fileid):
        sql = "SELECT id FROM uris WHERE file_id = {}".format(fileid)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getUri(self, uriId):
        sql = "SELECT path, filename FROM uris WHERE id = {}".format(uriId)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insertFile(self, fileChk):
        pass


BaseDatos = bdStore()
