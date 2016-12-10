#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3 as lite

class Utils:
    def almacenar_votacion(self,titulo, preguntas_respuestas):

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
            cur.execute("INSERT INTO Votacion(Nombre) VALUES(?)",titulo)
            votacionId = int(cur.execute("SELECT Votacion.id FROM Votacion WHERE Votacion.titulo == ?",titulo))

            # Crear preguntas para esa votación
            for pregunta in preguntas_respuestas:
                cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas,Id_votacion) VALUES(?,?,?)", pregunta, 50,votacionId)
                preguntaId = int(cur.execute("SELECT Pregunta.id FROM Pregunta WHERE Pregunta.texto == ?", pregunta))
                #Almacenar respuestas de
                for respuesta in preguntas_respuestas[pregunta]:
                    cur.execute("INSERT INTO RESPUESTA(Text,Veces_elegida,Id_pregunta) VALUES(?,?,?)", respuesta, 0, preguntaId)

