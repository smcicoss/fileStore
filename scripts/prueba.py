#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

prueba.py

Módulo librería para el acceso a la base de datos de
fileStore
"""

from libStore import constStore as cons
from libStore import configStore as cnf
from libStore import bdStore as bd

if __name__ == '__main__':
    print(cons.MSG_OK + "Script de pruebas de fileStore." + cons.MSG_END)
    print(cnf.conf)
