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
from flask import Flask, render_template


import wordsegment
from wordsegment import load, segment
load()
import nltk
nltk.download('vader_lexicon')

from tiktok_functions import make_scatterplot, clean_tiktok_df, get_sentiment, make_piechart


app = Flask(__name__)

def get_tiktok_db():
    ''' 
    A function that accesses the tiktok database through the Flask web app
    '''
    # connect to db
    g.tiktok_db = sqlite3.connect("tiktok.db")

    # return connection
    return g.tiktok_db

def app_scatterplot(num_days):
    ''' 
    A function that passes a scatter plot of the sentiment analysis scores to the view.html template
    '''
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
    fig = make_scatterplot(tiktoks)

    return fig

def app_piechart(num_days):
    ''' 
    A function that passes a pie chart of the sentiment analysis scores to the view.html template
    '''
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
    fig = make_piechart(tiktoks)

    return fig


@app.route("/")
def main():
    '''
    The app route that is called when the web app is first initialized
    '''
    return render_template('test.html')
    
@app.route('/submit1/', methods=['GET', 'POST'])
def submit1():
    '''
    The app route that is called when the user wants to view the sentiments
    of trending TikToks. Allows the user to specify the format the data is
    displayed in.
    '''

    if request.method == 'GET':
        return render_template('submit1.html')
    else:
        # get num_days
        num_days = request.form['num_days']
        try: 
            num_days = int(num_days)

            if num_days > 13:
                return render_template('submit1.html', errornum=True)
            

        except: 
            return render_template('submit1.html', error=True)
    

        # get plot type
        plot = request.form['plot']

        # scatter plot
        if plot == 'scatter':
            fig = app_scatterplot(num_days)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # pie chart
        else: 
            fig = app_piechart(num_days)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        return render_template('view1.html', graphJSON=graphJSON)


@app.route('/view1/')
def view1():
    '''
    The app route that is called so that the user can view the plot of sentiment scores.
    '''
    return render_template('view1.html', graphJSON=graphJSON)

@app.route('/about_us/')
def about_us():
    '''
    The app route that is called when the user clicks on the 'About Us' tab of the web app
    '''
    return render_template('about_us.html')

@app.route('/what/')
def what():
    '''
    The app route that is called when the user clicks on the 'Our Goal' tab of the web app
    '''
    return render_template('what.html')
    

    

    


