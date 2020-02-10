#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

prueba.py

Módulo librería para el acceso a la base de datos de
fileStore
"""

from libStore import constStore as cons
from libStore import configStore as cnf
from libStore import bdStore as bdcnf

if __name__ == '__main__':
    print(cons.MSG_OK + "Script de pruebas de fileStore." + cons.MSG_END)
    print("versión gestor Base de Datos:%s %s %s" %
          (cons.MSG_OK, bdcnf.version[0], cons.MSG_END))
    bdcnf.close()
    print("Path al almacén: %s%s%s" %
          (cons.MSG_OK, cnf.conf["storePath"], cons.MSG_END))