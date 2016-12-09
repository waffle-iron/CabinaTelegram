#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3 as lite
import sys

class Utils:
    def almacenar_encuesta(titulo,preguntas_respuestas):

        #Ruta donde se creará la base de datos. En sistemas UNIX-like será /home/username/votacion.db
        home = os.path.expanduser('~')
        path = home + '/votacion.db'

        #Crea una conexión con la base de datos establecida en la ruta. Si no existe la base de datos, se creará una nueva
        con = lite.connect(path)

        with con:

            cur = con.cursor()

            #Activar el soporte de sqlite3 para claves foráneas
            cur.execute("PRAGMA foreign_keys = ON")

            #Insertar los datos en la BD:

            #Crear votación
            cur.execute("INSERT INTO Votacion(Nombre) VALUES(%s)",titulo)
            votacionId = int(cur.execute("SELECT Votacion.id FROM Votacion WHERE Votacion.titulo == %s",titulo))

            #Crear preguntas para esa votación
            for pregunta in preguntas_respuestas:
                cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas) VALUES(%s,%d)",preguntas_respuestas[pregunta],50)
                preguntaId = int(cur.execute("SELECT Pregunta.id FROM Pregunta WHERE Pregunta.texto == %s", preguntas_respuestas[pregunta]))
                for pregunta, respuesta in preguntas_respuestas:
                    cur.execute("INSERT INTO RESPUESTA(Text,Id_pregunta) VALUES(%s,%d)",respuesta,preguntaId)


	