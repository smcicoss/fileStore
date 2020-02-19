#! /usr/bin/python3

# -*- coding: utf-8 -*-

u"""

configStore.py

Módulo librería para el fichero de configuración

"""

from libStore import constStore as cons
import json

conf = json.loads(open(cons.FILE_CONFIG).read())
