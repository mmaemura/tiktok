# TikTok Project Proposal 
Kelly Chen

Emma Bradley

Matthew Maemura

### Abstract

Over the past few years, the social media app “TikTok” has gained substantial popularity, and according to Cloudflare, was the most visited website in 2021 surpassing Google. In popular culture, TikTok is regarded as an addictive app and many users report spending hours scrolling through videos on TikTok. Since social media addiction is associated with anxiety and depression, we hope to closely examine the content posted on the app and the effect that it may have on its users. To do so, we will collect text data from trending TikToks including captions, hashtags, and sounds in order to analyze their sentiments.

### Planned deliverables

For full success, we plan to present our work in a web app that displays sentiment analysis on the top ~50 TikToks in real time. We will build a model to perform sentiment analysis on the TikTok transcriptions, and our sentiment analysis will be displayed in the form of interactive visualizations. For partial success, we will build a simple web app that presents visualizations on data we collected over the span of a month.

### Resources Required

We will use an Unofficial TikTok API, following this link: https://github.com/davidteather/TikTok-Api. From there, we will create a data set of potentially the top 50 trending TikToks each day collected over a one-month period. While the API can collect the TikToks’ creators, captions, hashtags, and sounds, since we are interested in analyzing the content through sentiment analysis, we will require a process to transcribe the audio from the sounds.
While trending TikToks collected may not be transcribeable, measuring the sentiment of instrumental music requires a different model than the one we plan on building. This would require us to use an additional model or filter out TikToks that cannot be transcribed. 

### Tools and Skills Required

First, to collect data, the API must be installed, and then we will be able to use our Python skills to navigate the dictionaries to collect the data. Next, we will need to learn to build a data set from which we will further develop our understanding of sentiment analysis. Our analysis will consist of visualizations using thorough and professional chart-making skills, and our findings will be presented in a web app, constructed through course and online sources on Flask and CSS.

### What you will Learn

First of all, our entire group is still relatively new to working as a team to complete programming tasks. While we all took PIC 16A and completed the penguins final project, none of us have ever used GitHub to compile our work and share it with others. During this project we therefore hope to strengthen our communication and teamwork skills, as the ability to collaboratively work on coding projects is an essential skill for the workforce. From a technical standpoint, we will gain experience with extracting live data from the internet with an API and cleaning the data to assemble our own dataset. Additionally, we anticipate that we will use the Natural Language Toolkit (NLTK), an NLP library used to analyze text. Since we are all relatively new to sentiment analysis, we will also strengthen our ability to teach ourselves how to use the necessary packages to accomplish our task. Furthermore, we will extend our experience in building models and web apps from PIC 16B.

### Risks

To go about analyzing the TikToks' sounds, the current working pipeline is to download the TikTok as an mp4 file, convert to and save locally as a wav file, then use an existing library to transcribe the audio into text. There are risks to downloading and managing storage space for hundreds of TikTok's and their audios. If problems arise, we will have to find another method to acquire the audio transcription.

In addition, as of right now we are analyzing trending TikTok’s at the time in which we use the API to extract data. We will make the assumption that the trending TikTok’s at that given time will be representative of the trending TikTok’s at any given time.

A limitation with our analysis may be that the sentiment of TikTok’s is dictated by non text signals, i.e music playing in the background, non transcribable text in the video, or emojis or emoticons. We may encounter issues with laughter or overlaid text (the non text-to-speech kind). Additionally, the video itself and none of the sounds or text could be the main contributor to its sentiment. It's possible there may not be enough text data for a given TikTok to predict a sentiment, requiring the download of more TikTok's to get enough encompassing data.

TikTok's trending videos may not be representative enough for what people consume. In the concept of 'The Long Tail', there may be a few big, trending videos, but there exist several orders of magnitude more niche videos with dedicated communities. Our analysis risks not capturing the majority of videos people consume, since they may primarily watch from the 'tail'.

### Ethics

As mentioned in the resource section, our use of audio transcription can have trouble with accents, potentially excluding minority groups as demonstrated in this TikTok. Even though TikTok has included the option of autotranscribing videos for the visually impaired, this technology is imperfect. Another factor to consider is the TikTok For You page and how the algorithm determines which TikToks to show its users. While more popular creators on the app tend to be white, this may cause bias that promotes white creators over others.

We may encounter foreign languages in our trending videos' text. We are unsure if we have to discard this data to perform sentiment analysis. Doing so, though, may exclude non english-speaking communities from our analysis. This would be unfortunate because the reach of TikTok is spread around the world.
The potential benefit of this project is producing research that shows the typical sentiment displayed from TikTok content. The users and the app developers can recognize the the type of content they promote on the app. While TikTok has posting restrictions on inappropriate or offensive content, this app is known to be addictive, taking a toll on emotional health. While the results of project may point to less use of TikTok, the app would not be substantially harmed from less screen time. Taking control of emotional health leads to better overall health. Promoting better uses of social media can also contribute to improving society.

### Tentative Timeline

Week 4 Thursday: project proposal due

Week 6 Thursday: initial project presentation: demonstrate our data acquisition through API and our audio transcription, show a simple functioning web app, find a relative tutorial for a sentiment analysis model

Week 8 Thursday: visualizations on exploratory analysis and sentiment analysis, integration of visualizations onto the web app

Week 10 Wednesday: full incorporation of presenting visualization on the web app in real time

Friday of Finals Week: GitHub repository due
