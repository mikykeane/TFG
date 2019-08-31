
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TFG: Vigilancia Tecnológica y Minería de Opiniones en RRSS
% Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación
% Realizado por: Miguel Keane Cañizares
% Contacto: miguekeca@correo.ugr.es
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""


from pymongo import MongoClient
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime

# Conectamos MongoDB la base de datos "TwitterStream"
connection = MongoClient('localhost', 27017)
db = connection.TwitterDisney1808
db.tweets.create_index("id", unique=True, dropDups=True)
collection = db.tweets



# Apartado que estaremos modificando constantemente. Palabras claves a descargar. Tambien sirven hashtags
#keywords = ['#wine', 'wine','claret', 'chardonnay', 'sauvignon', 'merlot', 'pinot noir', 'carbenet sauvignon', 'gewurztraimer', 'riesling' ]
keywords = ['Disney+' ]
# Idioma en que descargo. De momento ingles, pero trivial de cambiar si deseo
language = ['en']

# Mis claves personales de twitter. Si no puedo descargar mas tendre que usar otras cuentas para ir descargando en orden
consumer_key = "TOKEN"
consumer_secret = "TOKEN"
access_token = "TOKEN"
access_token_secret = "YOUR TOKEN"
# Aqui indicamos que solo decargue los tweets que encajen con mis keywords
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Cargamos los tweets en la trash_can
        trash_can = json.loads(data)
        if  not trash_can['text'].startswith('RT'):

            # Cogemos la info que queremos del tweet para guardarlo en la base de datos    NOTA: SI QUIERO MAS O MENOS INFO EN LOS TWEETS QUE DESCARGO, AQUI TENGO QUE TOCAR
            language = trash_can['lang']  # Idioma en el que esta el Tweet
            username = trash_can['user']['screen_name']  # El tweetero que escribe
            followers = trash_can['user']['followers_count']  # Los seguidores que tiene el tweetero  IMPORTANTE POR SI LUEGO QUIERO HACER ALGO CON ELLO
            tweet_id = trash_can['id_str']  # La ID del tweet en formato string
            hashtags = trash_can['entities']['hashtags']  # Hashtags que tenga el tweet
            if "extended_tweet" in trash_can:
                text = trash_can['extended_tweet']['full_text']
                print ("Entra a full text\n")
            else:
                text = trash_can['text']
            #text = trash_can['full_text']  # El tweet en si
            time_tweet = trash_can['created_at']  # Cuando se crea el tweet


            # A MongoDB no le gusta el formato del tiempo del tweet, asique lo convierto a un formato que le gusta mas y lo llamo time_for_mongo
            time_for_mongo = datetime.datetime.strptime(time_tweet, '%a %b %d %H:%M:%S +0000 %Y')


            # Junto toda la informacion en una variable tweet que sera la que guarde en la bd
            try:
                tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'time_for_mongo':time_for_mongo}

                # Guardo el tweet completo en MongoDB
                collection.insert_one(tweet)
            except:
                print("\nDuplicate Key Error\n")

            del tweet



            # Para gusto personal voy imprimiendo por pantalla los tweets que voy descargando segun los descargo en tiempo real
            print (username + ': ' + text)
            return True
        else:
            print("RETWEET\n")


    def on_error(self, status):
        print status


# Aqui se realiza la coneccion gracias a Tweepy con mis claves
if __name__ == '__main__':
    imlistening = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, imlistening, tweet_mode='extended')
    stream.filter(track=keywords, languages=language)
