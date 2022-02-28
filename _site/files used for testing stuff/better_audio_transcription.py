

from os import path
import requests

src = r'https://sf16-ies-music-va.tiktokcdn.com/obj/musically-maliva-obj/7040826800779414277.mp3'

r = requests.get(src)

with open('test.mp3', 'wb') as f:
    f.write(r.content)