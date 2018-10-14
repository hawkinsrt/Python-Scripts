# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 16:37:05 2018

@author: ejvpaba
"""
import pandas as pd
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, timedelta#, date, time
import config as cg

auth = OAuthHandler(cg.consumer_key, cg.consumer_secret)
auth.set_access_token(cg.access_token, cg.access_token_secret)
auth_api = API(auth)

account_list = ['OhNoSheTwitnt']
userdata_dict = {'Name': [], 'Screen_Name': [], 'Desc': [], 'Statuses': [],
                 'Friends': [], 'Followers': [], 'Member_for': [], 'TPD': []}


for target in account_list:
    item = auth_api.get_user(target)
    userdata_dict['Name'].append(item.name)
    userdata_dict['Screen_Name'].append(item.screen_name)
    userdata_dict['Desc'].append(item.description)
    userdata_dict['Statuses'].append(item.statuses_count)
    userdata_dict['Friends'].append(item.friends_count)
    userdata_dict['Followers'].append(item.followers_count)
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    userdata_dict['Member_for'].append(str(account_age_days) + ' days')
    TPD = float(tweets) / float(account_age_days)
    userdata_dict['TPD'].append(TPD)

hashtags = []
mentions = []
tweet_count = 0
end_date = datetime.utcnow() - timedelta(days=365)
for status in Cursor(auth_api.user_timeline, id=target).items():
  tweet_count += 1
  if hasattr(status, "entities"):
    entities = status.entities
    if "hashtags" in entities:
      for ent in entities["hashtags"]:
        if ent is not None:
          if "text" in ent:
            hashtag = ent["text"]
            if hashtag is not None:
              hashtags.append(hashtag)
    if "user_mentions" in entities:
      for ent in entities["user_mentions"]:
        if ent is not None:
          if "screen_name" in ent:
            name = ent["screen_name"]
            if name is not None:
              mentions.append(name)

yaztweets = auth_api.user_timeline(screen_name = 'OhNoSheTwitnt', count = 1000, include_rts = True)
yaztweets_dict = {'Retweet': [], 'Date': [], 'Retweets': [], 'Replying To': [],
                  'Tweet': []}

for status in yaztweets:

    if status.text[:2] == 'RT':
        yaztweets_dict['Retweet'].append('Y')
    else:
        yaztweets_dict['Retweet'].append('N')

    yaztweets_dict['Date'].append(status.created_at)
    yaztweets_dict['Retweets'].append(status.retweet_count)
    yaztweets_dict['Replying To'].append(status.in_reply_to_screen_name)
    yaztweets_dict['Tweet'].append(status.text)

userdata_df = pd.DataFrame(userdata_dict)
hashtags_df = pd.DataFrame(hashtags)
hashtags_df.columns = ['Hashtags_Used']
mentions_df = pd.DataFrame(mentions)
mentions_df.columns = ['Mentions']
yaztweets_df = pd.DataFrame(yaztweets_dict)

writer = pd.ExcelWriter(r'C:\Users\user\Documents\Python Scripts\data\OnNoSheTwitnt.xlsx')
userdata_df.to_excel(writer, index = False, sheet_name = 'User_Data')
hashtags_df.to_excel(writer, index = False, sheet_name = 'Hashtags')
mentions_df.to_excel(writer, index = False, sheet_name = 'Mentions')
yaztweets_df.to_excel(writer, index = False, sheet_name = 'Tweets')
writer.save()
