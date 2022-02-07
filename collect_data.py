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


##to run
##in C: ... \tiktok
##virtualenv env
##cd env\Scripts
##activate
##cd ..
##cd ..
##python collect_data.py

def get_tiktok_data(k = 1, get_transcription = False, to_db = False, to_csv = False):
    verifyFp = "verify_5ac3d7e61b6197794299a7ffda73bc33"

    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

    tiktoks = api.by_trending(count = k)

    py_file_path = os.path.dirname(os.path.realpath(__file__)) #full path to directory of this python file
    mp3_folder = r'/mp3_files/'
    wav_folder = '\wav_files\\'
    
    #time.sleep(1) to wait a sec

    conn = sqlite3.connect("tiktok.db")

    columns = ["date_pulled","id", "video_title", "video_url", 'upload_time',"creator", "creator_nickname", "creator_id", "creator_verified", "like", "share", "comment", "view", "original_item", "sound_id", "sound_title", "sound_author", "sound_orignal", "sound_url", "sound_transcribed"]
    df = pd.DataFrame(columns = columns)
    i = 0
    for tiktok in tiktoks:

        date = [datetime.datetime.now()]
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

            download_mp3(mp3_path, url = sound[4])
            mp3_to_wav(mp3_path, wav_path)
            sound[-1] = get_audio_transcription(wav_path)

        row = date + video + creator + stats + misc + sound

        df.loc[i] = row
        i += 1
        if i % 10 == 0:
            print(i)

    delete_audio_folder(py_file_path + mp3_folder)
    delete_audio_folder(py_file_path + wav_folder)

    if to_db:
        df.to_sql("tiktok", conn, if_exists = "append", index = False)

    if to_csv:
        return df.to_csv("{date[0]}.csv")


def download_mp3(mp3_path, url):
    r = requests.get(url)
    with open(mp3_path, 'wb') as f:
        f.write(r.content)

def mp3_to_wav(mp3_path, wav_path):
    try:    
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format = "wav")
    except Exception as e:
        print("encountered wav conversion error")
    

def get_audio_transcription(wav_path):
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
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))




get_tiktok_data(k = 100, get_transcription = True, to_db = True, to_csv = False)

