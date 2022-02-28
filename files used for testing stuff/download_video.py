from TikTokApi import TikTokApi
import pandas as pd
import string
import random
import os

verifyFp = "verify_5ac3d7e61b6197794299a7ffda73bc33"
did = ''.join(random.choice(string.digits) for num in range(19))

api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True, custom_device_id = did)

results = 2
tiktoks = api.by_trending(count = results)


music = api.get_music_object_full(tiktoks[1]['music']['id'])
print(music)

video_bytes = api.get_video_by_tiktok(tiktoks[0])

save_path = r'C:\Users\Matthew\Desktop\Senior Year\Winter\PIC 16B\tiktok\videos_folder'
file_name = "test.mp4"
complete_path = os.path.join(save_path, file_name)

with open(complete_path, "wb") as o:
    o.write(video_bytes)