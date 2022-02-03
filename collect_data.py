from TikTokApi import TikTokApi
import pandas as pd
import string
import random
import datetime
import requests
from pydub import AudioSegment
import os

def get_tiktok_data(k):
    verifyFp = "verify_5ac3d7e61b6197794299a7ffda73bc33"

    api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

    tiktoks = api.by_trending(count = k)


    #time.sleep(1) to wait a sec

    columns = ["date_pulled","id", "video_title", "video_url", 'upload_time',"creator", "creator_nickname", "creator_id", "creator_verified", "digg", "share", "comment", "play", "original_item", "sound_id", "sound_title", "sound_author", "sound_orignal", "sound_url", "sound_transcribed"]
    df = pd.DataFrame(columns = columns)
    i = 0
    for tiktok in tiktoks:

        date = [datetime.datetime.now()]
        video = [tiktok['id'], tiktok['desc'], tiktok['createTime'],tiktok['video']['playAddr']] 
        creator = [tiktok['author']['uniqueId'], tiktok['author']['nickname'], tiktok['author']['id'], tiktok['author']['verified']] 
        stats = [tiktok['stats']['diggCount'], tiktok['stats']['shareCount'], tiktok['stats']['commentCount'], tiktok['stats']['playCount']]
        misc = [tiktok['originalItem']]
        sound = [tiktok['music']['id'], tiktok['music']['title'], tiktok['music']['authorName'], tiktok['music']['original'], tiktok['music']['playUrl'], ""]

        row = date + video + creator + stats + misc + sound

        download_mp3(id = video[0], url = sound[4])
        get_audio_transcription(id = video[0])

        df.loc[i] = row
        i += 1

    #df.to_csv("first_csv.csv")
    return df.to_csv("second_csv.csv")


def download_mp3(id, url):
    py_file_path = os.path.dirname(os.path.realpath(__file__)) #full path to directory of this python file
    mp3_folder = r'/mp3_files/'
    mp3_file = f'{id}.mp3'
    full_path = py_file_path + mp3_folder + mp3_file
    
    r = requests.get(url)
    with open(full_path , 'wb') as f:
        f.write(r.content)

def get_audio_transcription(id):
    py_file_path = os.path.dirname(os.path.realpath(__file__))
    wav_folder = r'/wav_files/'
    mp3_folder = r'/mp3_files/'
    mp3_file = f'{id}.mp3'
    wav_file = f'{id}.wav'

    mp3_file_path = py_file_path + mp3_folder + mp3_file
    wav_file_path = py_file_path + wav_folder + wav_file

    print("file path is: ", mp3_file_path)

    #audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format = "wav")

get_tiktok_data(5)
