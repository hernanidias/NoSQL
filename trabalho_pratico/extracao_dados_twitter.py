import tweepy
import time
import pymongo
import json
import pandas as pd
from pandas import DataFrame

#Variaveis de conexao do Twitter
consumer_key='FWJtgXh93k8vXrzOB9Py1zB0N'
consumer_secret='C9yxOH6nfe454uWaWNF7hj8nPBdpBpJJSdrYn7uadxA0yVKwRK'
access_token_key='806615925554376704-MTQp3tieKS7SpCo9LYv0Aad6kEhs0OP'
access_token_secret='bsgRqWClhF8IjX9aIwirE4KcGwiX4KSLb2QGIHj8730QY'


#Autenticacao
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)


#Cria uma conexao com o MongoDB
client = pymongo.MongoClient('localhost',27017)

#Cria o database dbTwitter
db = client.dbTwitter

#busca os tweets da regiao de Belo Horizonte (raio de 30km). 
c = tweepy.Cursor(api.search,
                           lang="pt",
                           geocode="-19.9208300,-43.9377800,30km",
                           since="2015-01-01",
                           rpp=100
                           ).items()

while True:
    try:
        tweet = c.next()
#Criacao dos vetores auxiliares
        created = []
        texto = []
        texto_tmp = tweet.text
        texto.append(texto_tmp.encode("utf8"))
        created.append(tweet.created_at)       
#Armazena os vetores em um dataframe        
		df = pd.DataFrame({'Created':created,'Texto':texto})
#Tranforma o dataframe em um formato Json		
        records = json.loads(df.T.to_json()).values()
#Insere o objeto json na collection "collectionTwitter"
        db.collectionTwitter.insert(records)
    except tweepy.TweepError:
#Espera 15 minutos quando é excedido o limite de extracao do Twitter        
        time.sleep(905)
        continue
    except StopIteration:
        break







