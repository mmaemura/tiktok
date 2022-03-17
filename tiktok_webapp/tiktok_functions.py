import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import collections
from plotly import express as px
import numpy as np
from wordsegment import load, segment
import re

import wordsegment
from wordsegment import load, segment
load()

import nltk
nltk.download('vader_lexicon')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

def clean_tiktok_df(tiktoks):
    
    #fix column 'upload_time' -> 'video_url'
    tiktoks = tiktoks.rename(columns = {'upload_time' : 'video_url'})
    
    #remove duplicates
    dups = tiktoks['id'].duplicated(keep = 'last') #keep the most recent version of the tiktok
    tiktoks = tiktoks[np.invert(dups)]
    tiktoks = tiktoks.reset_index(drop = True)
    
    #remove rows with no video_title and no sound_transcribed
    tiktoks = tiktoks[(tiktoks["sound_transcribed"] != 'NA') | (tiktoks["video_title"] != '')]
    
    #replace 'NA' in sound_transcribed with ''
    tiktoks["sound_transcribed"] = [sound if sound != 'NA' else '' for sound in tiktoks["sound_transcribed"]]
    tiktoks = tiktoks.reset_index(drop = True)
    
    #replace hashtag phrase with predicted phrase with spaces added
    tiktoks['hashtags'] = [re.findall(r"#(\w+)",x) for x in tiktoks['video_title'] ] #create col for list of hashtag phrases
    tiktoks['predicted_hashtag_words'] = [segment(' '.join(x)) for x in tiktoks['hashtags']] #create col for list of predicted phrases of each hashtag
    tiktoks['predicted_hashtag_words'] = [' '.join(x) for x in tiktoks['predicted_hashtag_words']] #list -> string
    tiktoks['original_video_title'] = tiktoks['video_title'] #keep original title in new column
    tiktoks['video_title'] = [re.sub("#[A-Za-z0-9_]+","", x) for x in tiktoks['video_title']] #remove hashtagged phrases from title
    tiktoks['video_title'] = tiktoks['video_title'] + tiktoks['predicted_hashtag_words'] #new title where hashtag phrases are replaced with their predicted words

    #rank tiktoks in order of date pulled
    tiktoks['date_pulled'] = pd.to_datetime(tiktoks.date_pulled)
    tiktoks['date'] = tiktoks['date_pulled'].dt.date
    tiktoks['rank'] = tiktoks['date'].rank(method='dense')
    
    return tiktoks


def get_sentiment(tiktoks):

    # get sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    #combine title and sound_transcribed
    tiktoks['title_and_sound'] = tiktoks['video_title'].astype(str) + ' ' + tiktoks['sound_transcribed'].astype(str)

    # get each score
    tiktoks['Negative Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['neg'])
    tiktoks['Neutral Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['neu'])
    tiktoks['Positive Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['pos'])
    tiktoks['Compound Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['compound'])
    return tiktoks


def plotsentiments2(tiktoks): 
    #get start and end date
    start = tiktoks['date'].min().strftime('%m/%d/%Y')
    end = tiktoks['date'].max().strftime('%m/%d/%Y')
    
    # plot data
    fig = px.scatter(tiktoks,
                     x = 'Positive Sentiment',
                     y = 'Negative Sentiment',
                     color = 'Compound Sentiment',
                     color_continuous_scale = ['rgb(255,0,80)', 'rgb(255,255,255)', 'rgb(0,242,234)'],
                     range_color = (-1.1,1.1),
                     template = 'plotly_dark',
                     hover_name = 'original_video_title',
                     hover_data = ['Neutral Sentiment', 'Compound Sentiment', 'like', 'sound_transcribed'],
                     size = 'like',
                     title = f'''Sentiment Analysis on Trending TikToks
                     <br> <sup> TikToks from {start} - {end}</sup>''',
                     size_max = 8,
                     width = 800,
                     height = 600)
                     
    fig.update_traces(marker_sizemin = 3)

    fig.update_layout(
        font={
            'size': 14},
        title = {
            'x':0.1
        })

    return fig

def sent_scores(tiktoks):
    ss = [SentimentIntensityAnalyzer().polarity_scores(text) for text in tiktoks['title_and_sound']]
    add_dict = collections.Counter({'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0})
    # add up all the sentiment scores of all the tiktoks
    for s in ss:
        counter = collections.Counter(s)
        add_dict += counter
    dict_ss = dict(add_dict)
    # take the average score
    for k in dict_ss.keys():
        dict_ss[k] = dict_ss[k]/len(ss)

    return dict_ss

def make_piechart(tiktoks):
    # get date range
    start = tiktoks['date'].min().strftime('%m/%d/%Y')
    end = tiktoks['date'].max().strftime('%m/%d/%Y')

    dict_data = sent_scores(tiktoks).copy()
    dict_data.pop('compound')
    df_data = pd.DataFrame([{'sentiment': x, 'score': y} for x,y in dict_data.items()])
    fig = px.pie(df_data, 
                 names='sentiment', 
                 values='score', 
                 title = f'''Sentiment Analysis on Trending TikToks
                     <br> <sup> TikToks from {start} - {end}</sup>''', 
                 template = 'plotly_dark', 
                 color_discrete_sequence = ['rgb(255,255,255)', 'rgb(0,242,234)', 'rgb(255,0,80)'],
                 width = 800,
                 height = 600)
    return fig





