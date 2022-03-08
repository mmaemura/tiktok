'''
# Local Preview
At the command line: 

conda activate PIC16B
export FLASK_ENV=development; flask run

# Sources:
Lecture notes from class, and flask-examples repository from Professor Chodrow on GitHub
'''

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import collections
from plotly import express as px
import numpy as np
from wordsegment import load, segment

import io
import random

import plotly
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from plotly import express as px

from flask import Flask, render_template, request, g

import numpy as np
import re

import wordsegment
from wordsegment import load, segment
load()
import nltk
nltk.download('vader_lexicon')

from Emma_test import plotsentiments2, clean_tiktok_df, get_sentiment



app = Flask(__name__)

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
    
    return tiktoks

def get_tiktok_db():
    if 'tiktok_db' not in g:
        g.tiktok_db = sqlite3.connect("tiktok.db")
    #g.tiktok_db.execute('''CREATE TABLE IF NOT EXISTS tiktok(id INTEGER, video_title TEXT, sound_transcribed TEXT, upload_time TEXT, view INTEGER, date_pulled TEXT, like INTEGER)''')
    return g.tiktok_db

def plot_sentiments(days):
    # connetct to db
    g.tiktok_db = get_tiktok_db()

     # initialize c
    #mycursor = g.tiktok_db.cursor()

    #myconn = sqlite3.connect("tiktok.db")

    # get tik toks from past # of days
    cmd = \
    f"""
    SELECT id, video_title, upload_time, sound_transcribed, like, view
    FROM tiktok
    """ 

    tiktoks = pd.read_sql_query(cmd, g.tiktok_db)

    # close database
    g.tiktok_db.close()

    audio_tiktoks = tiktoks[tiktoks["sound_transcribed"] != "NA"]
    audio_tiktoks = audio_tiktoks.drop_duplicates(subset='id')

    ss = [SentimentIntensityAnalyzer().polarity_scores(title) for title in audio_tiktoks["video_title"]]

    add_dict = collections.Counter({'neu': 0.0, 'pos': 0.0, 'compound': 0.0, 'neg': 0.0})
    dict_ss = {}
    for s in ss:
        counter = collections.Counter(s)
        add_dict += counter
        dict_ss = dict(add_dict)

    # take the average score
    for k in dict_ss.keys():
        dict_ss[k] = dict_ss[k]/len(dict_ss)

    dict_data = dict_ss.copy()
    #dict_data.pop('compound')
    plt.pie(dict_data.values(), labels=dict_data.keys())
    #plt.show()

    return plt

def plot_sentiments2(num_days):
    g.tiktok_db = get_tiktok_db()
    #conn = sqlite3.connect("tiktok.db")
    cmd = \
    f"""
    SELECT id, video_title, upload_time, sound_transcribed, like, view
    FROM tiktok 
    """ 
    tiktoks = pd.read_sql_query(cmd, g.tiktok_db)
    #tiktoks = pd.read_sql_query(cmd, conn)

    # close database
    g.tiktok_db.close()
    #conn.close()
    tiktoks = clean_tiktok_df(tiktoks)
    tiktoks = get_sentiment(tiktoks)

    fig = plotsentiments2(tiktoks)
    print(tiktoks['view'])
    return fig


@app.route("/")
def main():
    return render_template('base.html')
    
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        #if request.form.get('action1') == 'go now!':
        return render_template('submit.html', thanks=True, num_days=request.form['num_days'])


@app.route('/view/')
def view2():
    fig = plot_sentiments2(10)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #fig.savefig('/static/new_plot.png')
   #return render_template('view.html', name = 'new_plot', url ='/static/Unknown.png')
    return render_template('view2.html', graphJSON=graphJSON)

@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')
    

    

    


