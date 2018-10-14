# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:24:17 2018

@author: user
"""

# Load JSON
import json

# Convert from JSON to Python object
tweet = json.loads('tweets_20181002-162341.json')

# Print tweet text
print(tweet['text'])

# Print tweet id
print(tweet['id'])