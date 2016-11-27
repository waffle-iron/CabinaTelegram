#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3 as lite
import sys

class Utils:
    def

#Ruta donde se creará la base de datos. En sistemas UNIX-like será /home/username/votacion.db
home = os.path.expanduser('~')
path = home + '/votacion.db'

#Crea una conexión con la base de datos establecida en la ruta. Si no existe la base de datos, se creará una nueva
con = lite.connect(path)

with con:

    cur = con.cursor()

    #Activar el soporte de sqlite3 para claves foráneas
    cur.execute("PRAGMA foreign_keys = ON")

	