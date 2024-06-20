from yt_video_transcript import get_transcript, download_video
from yt_short import overlay_videos_with_blur
import os
import logging

os.system('cls')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def deletar_arquivos(pasta):
    for filename in os.listdir(pasta):
        file_path = os.path.join(pasta, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"Arquivo {file_path} deletado.")
        except Exception as e:
            logging.info(f"Erro ao deletar o arquivo {file_path}: {e}")

def prompt_generator(transcript):
    last_start = transcript[-1]['start']
    div = float(last_start)/6
    dic_temp = {'content1':[],'content2':[],'content3':[],'content4':[],'content5':[],'content6':[]}
    for item in transcript:
        if item['start'] < div:
            dic_temp['content1'].append(item)
        elif div <= item['start'] < div * 2:
            dic_temp['content2'].append(item)
        elif div * 2 <= item['start'] < div * 3:
            dic_temp['content3'].append(item)
        elif div * 3 <= item['start'] < div * 4:
            dic_temp['content4'].append(item)
        elif div * 4 <= item['start'] < div * 5:
            dic_temp['content5'].append(item)
        else:
            dic_temp['content6'].append(item)
    
    template = {"content":[{
                "start_time": 1303.96,
                "end_time": 1337.039,
                "description": "terg 300"
                }]}

    for i in range(1, ((len(dic_temp))+1)):
        print(f'\nPrompt {i}')
        print('You are a ViralGPT helpful assistant.You are master at reading youtube transcripts and identifying the most Interesting and Viral Content\n')
        print(f"This is a transcript of a video. Please identify the 3 most viral sections from the whole, make sure they are more than 40 seconds in duration, Make Sure you provide extremely accurate timestamps respond only in this format {template}. Here is the Transcription:\n")
        print(dic_temp[f'content{i}'])
        print()
    logging.info('Prompts Gerados.')

video_id = 'XU_M2ih3VGw' #ID do video. Somente alterar aqui
filename = 'input_video.mp4'
diretorio = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\input\{video_id}_{filename}'
folder_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\finalcut'
temp_files = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\output'
json_files = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\json'

logging.info('Iniciando do programa:')
download_video(diretorio, video_id)
transcript = get_transcript(video_id)

cond = 0
if cond == 0:
    prompt_generator(transcript)
    logging.info('Fim do programa.')
else:
    #Alterar aqui para pegar os cortes.
    interesting_segment = {"content": [{"start_time": 243.079,"end_time": 280.16,"description": "Discussion about card cloning, Marcel's explanation of the 1995 card cloning operations, and the camaraderie and humor among the participants."}]}

    parsed_content = interesting_segment["content"]
    overlay_videos_with_blur(parsed_content, video_id)

    deletar_arquivos(temp_files)
    deletar_arquivos(json_files)
    logging.info('Fim do programa.')