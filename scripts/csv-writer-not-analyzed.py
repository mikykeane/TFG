"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TFG: Vigilancia Tecnológica y Minería de Opiniones en RRSS
% Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación
% Realizado por: Miguel Keane Cañizares
% Contacto: miguekeca@correo.ugr.es
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

# Hecha para crear tablas csv de bases de datos NO analizadas por MeaningCloud

from pymongo import MongoClient
import json
import datetime
import requests
import csv
import os.path

# Conectamos MongoDB la base de datos "TwitterStream"
connection = MongoClient('localhost', 27017)
db = connection.TwitterJdT
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets


#Me aserguro que el archivo no exista previamente, para no escribir varias veces los titulos
if not os.path.exists('data/JdT.csv'):
    with open('data/JdT.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(["Username,", 'Followers', 'Text'])

#
#cursors = db.collection.find();
#control = False
for cursor in db.tweets.find():
    tweet = cursor.get('text')
    username = cursor.get('username')
    followers = cursor.get('followers')

    print ('\n'+username + ': ' + tweet)
    quoted_tweet = '"{}"'.format(tweet)

    #a es para que sea "append" y no se sobreescriba lo ya escrito
    with open('data/JdT.csv', 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow([username, followers,  quoted_tweet])
