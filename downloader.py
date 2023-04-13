import pytube
import os
import requests
from tqdm import tqdm

# enter the URL of the YouTube video you want to download
url = input("Enter the YouTube video URL: ")

# create a YouTube object and get the audio stream
yt = pytube.YouTube(url)
audio_stream = yt.streams.filter(only_audio=True).first()

# download the audio stream and show the progress bar
audio_file = None
try:
    response = requests.get(audio_stream.url, stream=True)
    response.raise_for_status()
    with open('audio_temp', 'wb') as f:
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        for data in response.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            f.write(data)
    audio_file = 'audio_temp'
except (requests.exceptions.RequestException, pytube.exceptions.PytubeError) as e:
    print("Error downloading audio:", e)
    exit()

# convert the audio stream to an MP3 file
if audio_file is not None:
    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'
    os.rename(audio_file, new_file)
    print("Audio file saved as:", new_file)
else:
    print("Error converting audio: no file was downloaded")
