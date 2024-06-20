from pytube import YouTube
import os
import logging
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
os.system('cls')

def download_video(path, video_id):
    if not os.path.exists(path):
        url = 'https://www.youtube.com/watch?v='+video_id
        yt = YouTube(url)
        try:
            video = yt.streams.filter(progressive=True, file_extension='mp4')
            highest_resolution_stream = video.get_highest_resolution()
            highest_resolution_stream.download(filename=path)
            logging.info('Fim do download video.')
        except:
            video = yt.streams.first()
            video.download(filename=path)
            logging.info('Fim do download video.')
    else:
        logging.info('Arquivo já existe.')

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    logging.info('Transcrição pronta.')
    return transcript

