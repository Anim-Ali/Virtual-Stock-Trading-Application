import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import preprocessor as p
import statistics
from typing import List
from decimal import Decimal


# variables that contain user credentials to access twitter API
# Access token and secret
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
# API Keys
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
BEARER_TOKEN = ""

# Create authentication object
authentication = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# Set the access token and access token secret
authentication.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create the API object while passing in the auth information
api = tweepy.API(authentication, wait_on_rate_limit=True)


def get_tweets(keyword, number=100) -> List[str]:
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode="extended", lang="en").items(number):
        tweets.append(tweet.full_text)
    return tweets

def clean_tweets(tweets: List[str]) -> List[str]:
    clean = []
    for tweet in tweets:
        clean.append(p.clean(tweet))
    return clean

def get_sentiment(tweets: List[str]):
    sentiment_list = []
    for tweet in tweets:
        x = round(TextBlob(tweet).sentiment.polarity, 2)
        y = round(TextBlob(tweet).sentiment.subjectivity, 2)
        sentiment_list.append({'x': x,'y': y})
    
    return sentiment_list

# Create a function to compute negative, neutral and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

def getCount(analysis):
    Positive = 0
    Neutral = 0
    Negative = 0
    for each in analysis:
        if each == 'Positive':
            Positive += 1
        elif each == 'Neutral':
            Neutral += 1
        else:
            Negative += 1
    return [Positive, Neutral, Negative]


def get_data(keyword, number=100):
    tweets = get_tweets(keyword, number)
    clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(clean)

    analysis = []
    for i in range(len(tweets)):
        print(type(sentiment_scores[i]), sentiment_scores[i])
        analysis.append(getAnalysis(sentiment_scores[i].get('x')))

    counts = getCount(analysis)

    return counts, sentiment_scores 

