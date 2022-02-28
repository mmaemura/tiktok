# from pydub import AudioSegment
import subprocess

mp3_file_path = r'C:\Users\Matthew\Desktop\Git\tiktok\7037034323417107759.mp3'
# audio = AudioSegment.from_mp3(mp3_file_path)
# audio.export("test.wav", format = "wav")



subprocess.call(['ffmpeg', '-i', mp3_file_path, 'test.wav'])