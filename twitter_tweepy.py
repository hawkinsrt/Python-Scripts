# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:14:04 2018

@author: user
"""

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from config import *
import time


# Consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)

# Access key authentication
auth.set_access_token(access_token, access_token_secret)

# Set up the API with the authentication handler
api = API(auth)


class SListener(StreamListener):
    def __init__(self, api = None):
        self.output  = open('tweets_%s.json' %
            time.strftime('%Y%m%d-%H%M%S'), 'w')
        self.api = api or API()

# Set up words to track
keywords_to_track = ['#rstats','#python']

# Instantiate the SListener object 
listen = SListener(api)

# Instantiate the Stream object
stream = Stream(auth, listen)

# Begin collecting data
stream.filter(track = keywords_to_track)