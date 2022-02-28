
#pip install Wave
#pip install moviepy
#pip install SpeechRecognition


import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import os

transcribed_audio_file_name = "test.wav"
video_file_name = "test.mp4"

save_path = r'C:\Users\Matthew\Desktop\Senior Year\Winter\PIC 16B\tiktok\videos_folder'
file_name = "test.mp4"
complete_path = os.path.join(save_path, file_name)
video_file_name = complete_path

save_path = r'C:\Users\Matthew\Desktop\Senior Year\Winter\PIC 16B\tiktok\audios_folder'
file_name = "test.wav"
complete_path = os.path.join(save_path, file_name)
transcribed_audio_file_name = complete_path

audioclip = AudioFileClip(video_file_name)
audioclip.write_audiofile(transcribed_audio_file_name)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(transcribed_audio_file_name) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using google
try:
    print("Google thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google could not understand audio")
except sr.RequestError as e:
    print("Google error; {0}".format(e))
