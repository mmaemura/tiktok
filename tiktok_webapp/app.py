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

from tiktok_functions import plotsentiments2, clean_tiktok_df, get_sentiment


app = Flask(__name__)

def get_tiktok_db():
    if 'tiktok_db' not in g:
        g.tiktok_db = sqlite3.connect("tiktok.db")
    return g.tiktok_db

def plot_sentiments2(num_days):
    #connect to database
    g.tiktok_db = get_tiktok_db()
    
    cmd = \
    f"""
    SELECT id, video_title, upload_time, sound_transcribed, like, view, date_pulled
    FROM tiktok 
    """ 
    tiktoks = pd.read_sql_query(cmd, g.tiktok_db)

    # close database
    g.tiktok_db.close()

    # clean df
    tiktoks = clean_tiktok_df(tiktoks)
    tiktoks = tiktoks[tiktoks['rank'] <= num_days]

    # get sentiments
    tiktoks = get_sentiment(tiktoks)

    # plot sentiments
    fig = plotsentiments2(tiktoks)

    return fig


@app.route("/")
def main():
    return render_template('base.html')
    
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        # get num_days
        num_days = request.form['num_days']
        num_days = int(num_days)

        # scatter plot
        fig1 = plot_sentiments2(num_days)
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('view2.html', graphJSON=graphJSON)

@app.route('/view2/')
def view2():
    #fig = plot_sentiments2(10)
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('view2.html', graphJSON=graphJSON)

@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')

@app.route('/what/')
def what():
    return render_template('what.html')
    

    

    


