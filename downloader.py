import os
import pytube
import requests
from tqdm import tqdm
from urllib.parse import urlparse

# function to download a single audio file
def download_audio(url):
    try:
        # create a YouTube object and get the audio stream
        yt = pytube.YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # get the file name
        file_name = yt.title + '.mp3'

        # create the downloads directory if it does not exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # check if the file already exists
        filepath = os.path.join('downloads', file_name)
        if os.path.exists(filepath):
            print("The file", file_name, "already exists.")
            return

        # download the audio stream and show the progress bar
        response = requests.get(audio_stream.url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                f.write(data)
        print("Audio file saved as:", filepath)
    except (requests.exceptions.RequestException, pytube.exceptions.PytubeError) as e:
        print("Error downloading audio:", e)

# function to download all audio files from a playlist
def download_playlist(url):
    try:
        # create a YouTube playlist object
        playlist = pytube.Playlist(url)

        # loop through each video in the playlist and download its audio stream
        for video in playlist.videos:
            download_audio(video.watch_url)
    except pytube.exceptions.PytubeError as e:
        print("Error downloading playlist:", e)

# main program loop
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n============================")
        print(" YouTube Audio Downloader")
        print("============================")
        print("1. Download a single audio file")
        print("2. Download all audio files from a playlist")
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            url = input("Enter the YouTube video URL: ")
            if "youtube.com" in url.lower() and urlparse(url).scheme in ["http", "https"]:
                download_audio(url)
                input("\nPress Enter to continue...")
            else:
                print("Invalid YouTube URL. Please enter a valid YouTube URL.")
                input("\nPress Enter to continue...")
        elif choice == '2':
            url = input("Enter the YouTube playlist URL: ")
            if "youtube.com" in url.lower() and urlparse(url).scheme in ["http", "https"]:
                download_playlist(url)
                input("\nPress Enter to continue...")
            else:
                print("Invalid YouTube URL. Please enter a valid YouTube URL.")
                input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please enter '1' or '2'.")
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\nProgram canceled by user.")
        break

print("\nThank you for using YouTube Audio Downloader!")
