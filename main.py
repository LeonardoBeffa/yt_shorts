from yt_video_transcript import get_transcript, download_video
from yt_short import segment_video, detect_faces, crop_video
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
            print(f'Renamed: {item} -> {new_filename}')

video_id='YeZGYmtkvE4' #ID do video. Somente alterar aqui
filename = 'input_video.mp4'
diretorio = fr'C:\Users\Beffa\Documents\Python\AI-Shorts-Creator-main\input\{video_id}_{filename}'
folder_path = fr'C:\Users\Beffa\Documents\Python\AI-Shorts-Creator-main\output'

logging.info('Iniciando do programa:')
download_video(diretorio, video_id)
transcript = get_transcript(video_id)
print(transcript)

cond = 1
if cond == 0:
    logging.info('Fim do programa.')
else:
    #Alterar aqui para pegar os cortes.
    interesting_segment = {
        "content": [
    {
        "start_time": 1303.96,
        "end_time": 1337.039,
        "description": "terg 300"
    },
    ]

    }
    parsed_content = interesting_segment["content"]
    segment_video(parsed_content, video_id)

    for i in range(0, len(interesting_segment["content"])):  
        input_file = fr'AI-Shorts-Creator-main/output/{video_id}_output{str(i).zfill(3)}.mp4'
        output_file = fr'C:\Users\Beffa\Documents\Python\AI-Shorts-Creator-main\output_cropped\{video_id}_output_cropped{str(i).zfill(3)}.mp4'
        faces = detect_faces(input_file)
        crop_video(faces, input_file, output_file)
        logging.info('Fim do programa.')

make_unique_filenames(folder_path)
