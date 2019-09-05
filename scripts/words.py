"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TFG: Vigilancia Tecnológica y Minería de Opiniones en RRSS
% Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación
% Realizado por: Miguel Keane Cañizares
% Contacto: miguekeca@correo.ugr.es
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""


#Ejecutar con python3.7

# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt




#Datos que modificar para seleccionar ficheros existentes o nombres del fichero que será creado
csv="data/JdT.csv"

grafica="img/barraJdT.png"
modelo="img/rojo.jpg"
nube="img/jdT-red.png"

df = pd.read_csv(csv)

#print(df[df['Score_tag'].str.contains("N+")])
##score = df[df['Score_tag'].str.contains("N+|N|NEU|P|P+")].groupby('Score_tag')
score = df[~df['Score_tag'].isin(['NONE'])].groupby("Score_tag")
#score = df.groupby("Score_tag")
#score.filter( "NONE")
print(score.describe())
print(score.mean())

plt.figure(figsize=(15,10))
#score.size().sort_values(ascending=False).plot.bar()
score.size().plot.bar()

plt.xticks(rotation=50)
plt.xlabel("Score")
plt.ylabel("Tweets")
plt.savefig(grafica, format="png")
plt.show()





text = " ".join(text for text in df.Tweet)

print("Hay {} palabras en la combinacion de todos los tweets.".format(len(text)))

netflix_mask = np.array(Image.open(modelo))


#netflix_mask= convert_image("logo.png")
#converted = pure_pil_alpha_to_color_v2(image)

#netflix_mask = np.array(converted)

#wordcloud = WordCloud(max_font_size=50, max_words=100).generate(text)

# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["YouTube", "RT", "DNCNwIZDRZ", "12sSdRD08Oo" "amp", "co", "https"])

# Generate a word cloud image
#wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
wordcloud = WordCloud(background_color="white", max_words=1000000, mask=netflix_mask,
                        stopwords=stopwords, contour_width=2, contour_color='black')

wordcloud.generate(text)

#wordcloud.to_file("NetflixAll2.png")

image_colors = ImageColorGenerator(netflix_mask)
plt.figure(figsize=[7,7])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')

plt.axis("off")
plt.savefig(nube, format="png")
plt.show()
