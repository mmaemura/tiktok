from TikTokApi import TikTokApi
import pandas as pd
import string
import random

verifyFp = "verify_5ac3d7e61b6197794299a7ffda73bc33"

api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

results = 10
tiktoks = api.by_trending(count = results)


#time.sleep(1) to wait a sec

columns = ["id", "video_title", "video_url", "creator", "creator_nickname", "creator_id", "creator_verified", "digg", "share", "comment", "play", "original_item", "sound_id", "sound_title", "sound_author", "sound_orignal", "sound_url", "sound_transcribed"]
df = pd.DataFrame(columns = columns)
i = 0
for tiktok in tiktoks:
    video = [tiktok['id'], tiktok['desc'], tiktok['video']['playAddr']] 
    creator = [tiktok['author']['uniqueId'], tiktok['author']['nickname'], tiktok['author']['id'], tiktok['author']['verified']] 
    stats = [tiktok['stats']['diggCount'], tiktok['stats']['shareCount'], tiktok['stats']['commentCount'], tiktok['stats']['playCount']]
    misc = [tiktok['originalItem']]
    sound = [tiktok['music']['id'], tiktok['music']['title'], tiktok['music']['authorName'], tiktok['music']['original'], tiktok['music']['playUrl'], ""]

    row = video + creator + stats + misc + sound
    df.loc[i] = row
    i += 1

print(df.head(results))
df.to_csv("first_csv.csv")
#print(tiktoks[0]['music']['id'])