from TikTokApi import TikTokApi
import pandas as pd
import string
import random
import datetime
import requests
from pydub import AudioSegment
import speech_recognition as sr
import os
import sqlite3
import shutil


def get_tiktok_data(verifyFp, k = 1, get_transcription = False, to_db = False, db_file_name = "tiktok.db", to_csv = False):
    """
    Purpose is to query the top k trending tiktoks and store their information.
    verifyFP is found on Chrome when you visit tiktok.com (tutorial by API devoloper here: https://www.youtube.com/watch?v=zwLmLfVI-VQ&t=2s).
    If get_transcription is True then we download the audio files and run them through a sound transcriptor.
    If to_db is True we store tiktok information in database file called db_file_name.
    If to_csv is True we store tiktok information in csv.
    """
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

    tiktoks = api.by_trending(count = k) #json dictionary for information of all k tiktoks

    py_file_path = os.path.dirname(os.path.realpath(__file__)) #full path to directory of this python file
    mp3_folder = r'/mp3_files/'
    wav_folder = r'wav_files/'

    #our desired information from the tiktoks
    columns = ["date_pulled","id", "video_title", "upload_time", 'video_url',"creator", "creator_nickname", "creator_id", "creator_verified", "like", "share", "comment", "view", "original_item", "sound_id", "sound_title", "sound_author", "sound_orignal", "sound_url", "sound_transcribed"]
    df = pd.DataFrame(columns = columns)
    i = 0
    for tiktok in tiktoks:

        date = [datetime.datetime.now()]

        #list components for our data
        video = [tiktok['id'], tiktok['desc'], tiktok['createTime'],tiktok['video']['playAddr']] 
        creator = [tiktok['author']['uniqueId'], tiktok['author']['nickname'], tiktok['author']['id'], tiktok['author']['verified']] 
        stats = [tiktok['stats']['diggCount'], tiktok['stats']['shareCount'], tiktok['stats']['commentCount'], tiktok['stats']['playCount']]
        misc = [tiktok['originalItem']]
        sound = [tiktok['music']['id'], tiktok['music']['title'], tiktok['music']['authorName'], tiktok['music']['original'], tiktok['music']['playUrl'], ""]

        if get_transcription:
            id = video[0]
            mp3_file = f'{id}.mp3'
            wav_file = f'{id}.wav'
            mp3_path = py_file_path + mp3_folder + mp3_file
            wav_path = py_file_path + wav_folder + wav_file

            download_mp3(mp3_path, url = sound[4]) #download the audio file
            mp3_to_wav(mp3_path, wav_path) #convert from .mp3 to .wav
            sound[-1] = get_audio_transcription(wav_path) #last entry in sound corresponds to 'sound_transcribed' column; get transcribed sound

        #full data observation
        row = date + video + creator + stats + misc + sound

        df.loc[i] = row #append to dataframe
        i += 1
        if i % 10 == 0:
            print(i)

    #delete the audio files that we downloaded
    if get_transcription:
        delete_audio_folder(py_file_path + mp3_folder)
        delete_audio_folder(py_file_path + wav_folder)

    #append dataframe to the database
    if to_db:
        conn = sqlite3.connect(db_file_name)#connection to database
        df.to_sql("tiktok", conn, if_exists = "append", index = False)
        conn.close()
    
    #return a csv
    if to_csv:
        return df.to_csv("{date[0]}.csv")


def download_mp3(mp3_path, url):
    """
    download .mp3 file from the web through url and save as mp3_path
    """
    r = requests.get(url)
    with open(mp3_path, 'wb') as f:
        f.write(r.content)

def mp3_to_wav(mp3_path, wav_path):
    """
    mp3_path is existing .mp3 file on system. Convert to .wav file and save to wav_path
    """
    try:    
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format = "wav")
    except Exception as e:
        print("encountered wav conversion error")
    

def get_audio_transcription(wav_path):
    """
    wav_path is existing .wav file on system. Attempt to transcribe its audio.
    If successful then return transcribed audio. If non transcribable or file doesn't exist,
    return "NA".
    """
    exists = os.path.isfile(wav_path)
    if exists:
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "NA"
        except sr.RequestError as e:
            print("Google error; {0}".format(e))
    else:
        return "NA"

def delete_audio_folder(folder):
    """
    folder is system location for a folder. Delete all the contents in the folder.
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))