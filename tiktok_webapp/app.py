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

import io
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from flask import Flask, render_template, request, g
app = Flask(__name__)

def get_tiktok_db():
    g.tiktok_db = sqlite3.connect("tiktok.db")
    g.tiktok_db.execute('''CREATE TABLE IF NOT EXISTS tiktoks(id INTEGER, video_title TEXT, sound_transcribed TEXT, upload_time TEXT, view INTEGER, date_pulled TEXT)''')
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
    SELECT id, video_title, sound_transcribed, upload_time, view, date_pulled
    FROM tiktoks
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
    plot = plt.pie(dict_data.values(), labels=dict_data.keys())
    #plt.show()

    plt.savefig('new_plot.png')

    return plot

@app.route("/")
def main():
    return render_template('base.html')
    
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            return render_template('submit.html', thanks=True, num_days=request.form['num_days'])
        except:
            return render_template('submit.html', error=True)


@app.route('/view/')
def view():
    fig = plot_sentiments(10)
    return render_template('view.html', name = 'new_plot', url ='new_plot.png')

@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')
    

    

    


