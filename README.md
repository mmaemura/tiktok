# TikTok Sentiment Analysis Webapp

Kelly Chen

Emma Bradley

Matthew Maemura




We created a webapp to display our sentiment analysis on trending Tiktoks. 

## Launching the webapp
To launch the webapp on your browser, first fork this github repository so that the necessary files are on your device. Next, open the forked repository in GitHub Desktop and launch a corresponding terminal window. In the resulting terminal window, also enter the command: “cd tiktok_webapp” to navigate to the file containing the web app. In addition, enter the command “conda activate PIC16B” to ensure that you are working in your PIC16B environment. Lastly, run the following command: “export FLASK_ENV=development; flask run”. A link will be outputted, and you can now enter this link into a browser window and view our webapp!

## Navigating the webapp
First, click on the “Get Started” button on the home page. Next, you will be asked which type of plot you wish to view (scatter plot or pie chart) and the number of days worth of trending TikToks you would like to view. Click the “Go Now” button to view the resulting plot. A limitation of our app is that we only have 13 days worth of trending TikTok data. As a result, if the user enters a number greater than 13, an error message is returned. In addition, if the user inputs something that is not a number (ex: one), a different error message is returned asking the user to rephrase their input as a numeric value. In the navigation bar of our web app, we have also included a link to an “about us” page as well as an “our goal” page where we discussed our project’s goals, sentiment analysis and how we were able to apply it, as well as cited our sources. 

## Creating the database

We leveraged an unofficial TikTok API by David Teather, found here: https://github.com/davidteather/TikTok-Api . Note that we used version 4 of his API and he has since updated to version 5. Through this, we were able to query information (e.g title, author, number of likes, audio, video) on the top 100 trending TikToks from 2/5/22 - 2/19/22. Next, we use the audio files of the TikToks and transcribe them through the SpeechRecognition library. 

## Performing sentiment analysis

Sentiment analysis is a form of natural language processing (NLP) in which the computer is able to detect the emotional tone inferred from the text. In our project, we use VADER that was specifically built to analyze the sentiment of text used in social media. For our purposes, we determine the positive-negative sentiment from trending Tiktoks based on each Tiktok’s text compilation of its caption and audio transcription.

## Potential biases and limitations

We took the “trending” TikToks from the unofficial TikTok API in which the videos are ranked using TikTok’s algorithm. TikTok may promote certain types of content through their algorithm that may produce biases.

We use Google Speech Recognition for the English language. With user consent, Google devices and programs take audio samples, humans transcribe some of them, and the model gets trained in supervised learning. We noticed that the model has difficulty with transcribing accents and does not recognize foreign languages.

Using VADER Lexicon, the Sentiment Scores derived from Amazon Mechanical Turk, which has been known for crowdsourcing work that can be menial and low-paying.

## Sources

https://github.com/davidteather/TikTok-Api
https://pypi.org/project/SpeechRecognition/
https://pypi.org/project/wordsegment/
https://github.com/cjhutto/vaderSentiment
https://github.com/pure-css/pure/
