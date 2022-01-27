# TikTok Project Proposal 
Kelly Chen

Emma Bradley

Matthew Maemura

### Abstract
Over the past few years, the social media app “TikTok” has gained substantial popularity, and it currently boasts an impressive 1 billion users per month. In popular culture, TikTok is regarded as an addictive app and many users report spending hours scrolling through videos on TikTok. Since social media addiction is associated with anxiety and depression, we hope to closely examine the content posted on the app and the effect that it may have on users. To do so, we will collect text data from each TikTok including captions, hashtags, and sounds in order to identify the sentiments associated with trending TikTok’s.

### Planned deliverables
For full success, we plan to present our work in a Jupyter notebook that we will push to the web as a blog post on our websites. The blog will discuss our data collection process and analysis on the data, incorporating interactive charts. For partial success, we can still present the data we collected, and the quantity and quality of our charts may be lower. 

### Resources Required
We will use an Unofficial TikTok API linked here. From there, we will create a data set of the top 50 trending TikToks each day collected over a one week period. While the API can collect the TikToks’ creators, captions, hashtags, and sounds, since we are interested in analyzing the content through sentiment analysis, we will require a process to transcribe the audio from the sounds. 

### Tools and Skills Required
First, to collect data, the API must be installed, and then we will be able to use our Python skills to navigate the dictionaries to collect the data. Next, we will need to learn to build a data set from which we will further develop our understanding of sentiment analysis. Our analysis will consist of visualizations and will be presented as a blog post, using thorough and professional chart-making skills.

### What you will Learn
First of all, our entire group is still relatively new to working as a team to complete programming tasks. While we all took PIC 16A and completed the penguins final project, none of us have ever used GitHub to compile our work and share it with others. During this project we therefore hope to strengthen our communication and teamwork skills, as the ability to collaboratively work on coding projects is an essential skill for the workforce. From a technical standpoint, we will gain experience with extracting live data from the internet with an API and cleaning the data to assemble our own dataset. Additionally, we anticipate that we will use the Natural Language Toolkit (NLTK), an NLP library used to analyze text. Since we are all relatively new to sentiment analysis, we will also strengthen our ability to teach ourselves how to use the necessary packages to accomplish our task. 

### Risks
	We are still unsure how we will go about analyzing the TikTok sounds (audio). Upon first inspection, we suspect that we may need to download the MP3 file and then run it through another program to extract the audio transcription. Downloading the MP3 file for each trending TikTok will most likely take a decent amount of storage, so this is something that we are currently considering. We expect that this will affect the size of the dataset of trending TikTok’s that we choose to analyze. 
	In addition, as of right now we are analyzing trending TikTok’s at the time in which we use the TikTok API to extract data. We will make the assumption that the trending TikTok’s at that given time will be representative of the trending TikTok’s at any given time. 
	A limitation with our analysis may be that the sentiment of TikTok’s is dictated by non text signals, i.e music playing in the background or non transcribable text in the video. We may encounter issues with laughter or overlaid text (the non text-to-speech kind). Additionally, the video itself and none of the sounds or text could be the main contributor to its sentiment.

### Ethics
As mentioned in the resource section, our use of audio transcription can have trouble with accents, potentially excluding minority groups as demonstrated in this TikTok. Even though TikTok has included the option of autotranscribing videos for the visually impaired, this technology is imperfect. Another factor to consider is the TikTok For You page and how the algorithm determines which TikToks to show its users. While more popular creators on the app tend to be white, this may cause bias that promotes white creators over others. 
The potential benefit of this project is producing research that shows the typical sentiment displayed from TikTok content. The users and the app developers can recognize the the type of content they promote on the app. While TikTok has posting restrictions on inappropriate or offensive content, this app is known to be addictive, taking a toll on emotional health. While the results of project may point to less use of TikTok, the app would not be substantially harmed from less screen time. Taking control of emotional health leads to better overall health. Promoting better uses of social media can also contribute to improving society. 

### Tentative Timeline
Week 4 Thursday: project proposal due 
Week 6 Thursday: demonstrate our data acquisition through API and our audio transcription 
Week 8 Thursday: visualizations on exploratory analysis and sentiment analysis
Week 10 Wednesday: full incorporation into a blog post hosted on the web
Friday of Finals Week: GitHub repository due

