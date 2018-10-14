# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 19:16:51 2018

@author: user
"""

import pandas as pd

file = r'C:\Users\user\Documents\Python Scripts\data\Video_Games_5.json'
df = pd.read_json(file, lines = True)
cols = list(df.columns)
df['reviewTime'] = pd.to_datetime(df['reviewTime'], format='%m %d, %Y')

reviewdf = df[['asin', 'overall', 'summary', 'reviewText', 'reviewTime']]
cols_list = ['Item', 'Stars', 'Title', 'Review', 'Date']
reviewdf.columns = cols_list

print(reviewdf.head())