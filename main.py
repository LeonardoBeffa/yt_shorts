from yt_video_transcript import get_transcript, download_video
from yt_short import overlay_videos_with_blur, remove_black_borders#segment_video_full, detect_faces, crop_video
import os
import logging
import random
import string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
os.system('cls')

def make_unique_filenames(folder_path):
    # Lista os itens na pasta
    items = os.listdir(folder_path)
    
    # Processa cada item na pasta
    for item in items:
        # Verifica se é um arquivo
        if os.path.isfile(os.path.join(folder_path, item)):
            # Separa o nome do arquivo e a extensão
            filename, extension = os.path.splitext(item)
            
            # Gera um valor aleatório para adicionar ao nome do arquivo
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Constrói o novo nome de arquivo único
            new_filename = f'{filename}_{random_suffix}{extension}'
            
            # Renomeia o arquivo com o novo nome
            os.rename(os.path.join(folder_path, item), os.path.join(folder_path, new_filename))
            logging.info(f'Renamed: {item} -> {new_filename}')

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

video_id='G40p0j4QaZg' #ID do video. Somente alterar aqui
filename = 'input_video.mp4'
diretorio = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\input\{video_id}_{filename}'
folder_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\output'
deleted_past = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\output_cropped'

logging.info('Iniciando do programa:')
download_video(diretorio, video_id)
transcript = get_transcript(video_id)

cond = 1
if cond == 0:
    prompt_generator(transcript)
    logging.info('Fim do programa.')
else:
    #Alterar aqui para pegar os cortes.
    interesting_segment = {"content": [{"start_time": 46.76,"end_time": 91.24,"description": "Introduction and humorous banter about the participants' professions, with jokes about physical appearance and age."}]}

    parsed_content = interesting_segment["content"]
    overlay_videos_with_blur(parsed_content, video_id)

    for i in range(0, len(interesting_segment["content"])):  
        input_file = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\output\{video_id}_output{str(i).zfill(3)}.mp4'
        output_file = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\output_cropped\{video_id}_output_cropped{str(i).zfill(3)}.mp4'
        #faces = detect_faces(input_file)
        #crop_video(faces, input_file, output_file)

    #make_unique_filenames(folder_path)
    #deletar_arquivos(deleted_past)
    logging.info('Fim do programa.')