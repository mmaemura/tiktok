'''
# Local Preview
At the command line: 

conda activate PIC16B
export FLASK_ENV=development; flask run

# Sources:
Lecture notes from class, and flask-examples repository from Professor Chodrow on GitHub
'''
import sqlite3

from flask import Flask, render_template, request, g
app = Flask(__name__)

def get_tiktok_db():
    g.tiktok_db = sqlite3.connect("tiktok.db")
    g.tiktok_db.execute('''CREATE TABLE IF NOT EXISTS tiktoks(id INTEGER, video_title TEXT, sound_transcribed TEXT, upload_time TEXT, view INTEGER, date_pulled TEXT)''')
    return g.tiktok_db

def plot_sentiments(days):
    # connetct to db
    g.tiktok_db = get_tiktok_db()

     # initialize cursor
    cursor = g.tiktok_db.cursor()

    # get tik toks from past # of days
    cmd = \
    f"""
    SELECT id, video_title, sound_transcribed, upload_time, view, date_pulled
    FROM tiktok
    """ 

    df = pd.read_sql_query(cmd, cursor)

    # close database
    g.message_db.close()

    return none

@app.route("/")
def main():
    return render_template('submit.html')
    
# getting messages
@app.route('/submit/', methods=['GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        return render_template('base.html')

    

    


