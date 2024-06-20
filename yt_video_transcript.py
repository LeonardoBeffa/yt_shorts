from pytube import YouTube
import os
import logging
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
os.system('cls')

def download_video(filename, video_id):
    url = 'https://www.youtube.com/watch?v='+video_id
    yt = YouTube(url)
    video = yt.streams.first()
    video.download(filename=filename)
    logging.info('Fim do download video.')

def get_transcript(video_id):
    # Obter a transcrição para o ID do vídeo fornecido
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    logging.info('get transcript')
    return transcript

