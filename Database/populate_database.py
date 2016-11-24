#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3 as lite
import sys



#Ruta donde debe estar la base de datos. En sistemas UNIX-like será /home/username/votacion.db
home = os.path.expanduser('~')
path = home + '/votacion.db'

#Crea una conexión con la base de datos establecida en la ruta. Si no existe la base de datos, se creará una nueva
con = lite.connect(path)

with con:

    cur = con.cursor()

    #Activar el soporte de sqlite3 para claves foráneas
    cur.execute("PRAGMA foreign_keys = ON")

    #Insertar datos en la tabla de Usario
    cur.execute("INSERT INTO Usuario(Telegram_id) VALUES(220)")
    cur.execute("INSERT INTO Usuario(Telegram_id) VALUES(230)")
    cur.execute("INSERT INTO Usuario(Telegram_id) VALUES(240)")
    cur.execute("INSERT INTO Usuario(Telegram_id) VALUES(250)")

    #Insertar datos en la tabla de Encuesta
    cur.execute("INSERT INTO Encuesta(Nombre) VALUES('Encuesta1')")
    cur.execute("INSERT INTO Encuesta(Nombre) VALUES('Encuesta2')")
    cur.execute("INSERT INTO Encuesta(Nombre) VALUES('Encuesta3')")
    cur.execute("INSERT INTO Encuesta(Nombre) VALUES('Encuesta4')")

    #Insertar datos en la tabla de Participación
    cur.execute("INSERT INTO Participacion(Id_usuario,Id_encuesta) VALUES(2,1)")
    cur.execute("INSERT INTO Participacion(Id_usuario,Id_encuesta) VALUES(2,1)")
    cur.execute("INSERT INTO Participacion(Id_usuario,Id_encuesta) VALUES(3,2)")
    cur.execute("INSERT INTO Participacion(Id_usuario,Id_encuesta) VALUES(3,3)")


    #Insertar datos en la tabla dePregunta
    cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas,Id_encuesta) VALUES('¿Qué hora es?',2,1)")
    cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas,Id_encuesta) VALUES('¿Cuántos años tienes?',4,2)")
    cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas,Id_encuesta) VALUES('¿Te gusta el yogur de fresa?',6,3)")
    cur.execute("INSERT INTO Pregunta(Texto,Max_respuestas,Id_encuesta) VALUES('¿Si o que?',8,4)")

    #Insertar datos en la tabla de Respuesta
    cur.execute("INSERT INTO Respuesta(Texto,Veces_elegida,Id_pregunta) VALUES('Las 12',5,1)")
    cur.execute("INSERT INTO Respuesta(Texto,Veces_elegida,Id_pregunta) VALUES('Más de 50',6,2)")
    cur.execute("INSERT INTO Respuesta(Texto,Veces_elegida,Id_pregunta) VALUES('Sí',7,3)")
    cur.execute("INSERT INTO Respuesta(Texto,Veces_elegida,Id_pregunta) VALUES('¿que?',8,1)")