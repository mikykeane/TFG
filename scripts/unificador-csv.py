"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TFG: Vigilancia Tecnológica y Minería de Opiniones en RRSS
% Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación
% Realizado por: Miguel Keane Cañizares
% Contacto: miguekeca@correo.ugr.es
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

#Este código es para coger todos los tweets ya analizados y juntar todos en una base de datos, hay que cambiar a la base de datos MongoDB deseada
# Solo funcionará con aquellas ya analizadas por MeaningCloud y con la conlección concepts creada.

from pymongo import MongoClient
import json
import datetime
import requests
import csv
import os.path

# Conectamos MongoDB la base de datos "TwitterStream"
connection = MongoClient('localhost', 27017)
db = connection.TwitterHBO1308
db.tweets.create_index("id", unique=True, dropDups=True)
collection = db.tweets
collection2 = db.concepts


#Me aserguro que el archivo no exista previamente, para no escribir varias veces los titulos
if not os.path.exists('data/HBO1308-notext.csv'):
    with open('data/HBO1308-notext.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['Username', 'Followers', 'Score_tag'])

#
#cursors = db.collection.find();
#control = False
for cursor in db.concepts.find():
      tweet = cursor.get('text')
      username = cursor.get('user')
      followers = cursor.get('followers')
      
      #quoted_tweet = '"{}"'.format(tweet)
      score_tag= cursor.get('score_tag')
      #El parametro a es para "append", para actualizar el csv en vez de sobrescribirlo
      with open('data/HBO1308-notext.csv', 'a') as csvfile:

          filewriter = csv.writer(csvfile, delimiter=',')
          filewriter.writerow([username, followers,  score_tag])
