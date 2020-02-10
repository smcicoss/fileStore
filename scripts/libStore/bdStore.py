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

db = pymysql.connect(cnf.conf["dbHost"], cnf.conf["dbUser"],
                     cnf.conf["dbPasswd"], cnf.conf["baseDatos"])

# prepara un objeto cursor usando el metodo  cursor()
cursor = db.cursor()

# ejecuta el SQL query usando el metodo execute().
cursor.execute("SELECT VERSION()")

# procesa una unica linea usando el metodo fetchone().
version = cursor.fetchone()


def close():
    # desconecta del servidor
    db.close()
