#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

bdStore.py

Módulo librería para el acceso a la base de datos de
fileStore
"""

import pymysql

# from libStore import constStore as cons
from libStore import configStore as cnf


class bdStore(object):

    def __init__(self):
        # Establece conexión con base de datos
        self.__conect = pymysql.connect(
            cnf.conf["dbHost"], cnf.conf["dbUser"],
            cnf.conf["dbPasswd"], cnf.conf["baseDatos"])

        # prepara un objeto cursor usando el metodo cursor()
        cursor = self.__conect.cursor()

        # ejecuta el SQL query usando el metodo execute().
        cursor.execute("SELECT VERSION()")

        # procesa una unica linea usando el metodo fetchone().
        self.version = cursor.fetchone()

    def __del__(self):
        # desconecta del servidor
        self.__conect.close()
