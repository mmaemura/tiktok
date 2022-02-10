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

@app.route("/")
def main():
    return render_template('base.html')
    
# getting messages
@app.route('/submit/', methods=['GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        return render_template('base.html')

    

    


