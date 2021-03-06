#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

constStore.py

definición de constantes.

"""

# codigos de retorno
RET_OK = 0
RET_CANCEL = 1
RET_ABORT = 2
ERROR_INTERNAL = 127
ERROR_NO_EJECUTABLE = 10
ERROR_NO_SOURCE_DIR = 11
ERROR_NO_VARIABLES = 12
ERROR_NO_PERMITIDO = 20
ERROR_FIND = 21
ERROR_FILE = 22
ERROR_DB = 30
ERROR_SQL = 31

# secuencias de ecape para colorear salida
MSG_OK = "\033[0;40;32m"
MSG_ALERT = "\033[1;40;33m"
MSG_WARNING = "\033[0;40;33m"
MSG_ERROR = "\033[0;40;31m"
MSG_END = "\033[0m"

# fichero de configuración
FILE_CONFIG = "/etc/fileStore/fileStore.conf.json"
