#!/usr/bin/env python
# coding: utf-8


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
    sid = SentimentIntensityAnalyzer()
    #combine title and sound_transcribed
    tiktoks['title_and_sound'] = tiktoks['video_title'].astype(str) + ' ' + tiktoks['sound_transcribed'].astype(str)

    tiktoks['Negative Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['neg'])
    tiktoks['Neutral Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['neu'])
    tiktoks['Positive Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['pos'])
    tiktoks['Compound Sentiment'] = tiktoks['title_and_sound'].apply(lambda x: sid.polarity_scores(x)['compound'])
    return tiktoks


def plotsentiments2(tiktoks): 
    start = tiktoks['date'].min().strftime('%m/%d/%Y')
    end = tiktoks['date'].max().strftime('%m/%d/%Y')

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
    # fig.update_xaxes(range=[-0.1,1.1])
    # fig.update_yaxes(range=[-0.1,1.1])
    fig.update_traces(marker_sizemin = 3)

    fig.update_layout(
        font={
            'size': 14},
        title = {
            'x':0.1
        })

    return fig





