from yt_video_transcript import get_transcript, download_video
from yt_short import overlay_videos_with_blur
import os
import logging

os.system('cls')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

video_id = 'G40p0j4QaZg' #ID do video. Somente alterar aqui
relative_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator' #Altere para a pasta do prejeto.

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

def verifica_ou_cria_pasta(past_path):
    if not os.path.exists(past_path):
        os.makedirs(past_path)
        logging.info(f'Pasta "{past_path}" criada com sucesso.')
    else:
        logging.info(f'A pasta "{past_path}" já existe.')

filename = 'input_video.mp4'
input_path = fr'{relative_path}\input\{video_id}_{filename}'
temp_files = fr'{relative_path}\output'
json_files = fr'{relative_path}\json'

logging.info('Iniciando do programa:')

verifica_ou_cria_pasta(fr'{relative_path}\input')
verifica_ou_cria_pasta(fr'{relative_path}\final')
verifica_ou_cria_pasta(fr'{relative_path}\pngs')
verifica_ou_cria_pasta(temp_files)
verifica_ou_cria_pasta(json_files)

download_video(input_path, video_id)
transcript = get_transcript(video_id)

cond = 0
if cond == 0:
    prompt_generator(transcript)
    logging.info('Fim do programa.')
else:
    #Alterar aqui para pegar os cortes.
    interesting_segment = {"content": [{"start_time": 46.76,"end_time": 91.24,"description": "Introduction and humorous banter about the participants' professions, with jokes about physical appearance and age."},{"start_time": 171.28,"end_time": 218.56,"description": "Discussion about participants' motivations to become police officers, with humorous and serious reflections."},{"start_time": 245.2,"end_time": 289.84,"description": "Continuation of personal stories and humorous exchanges about being police officers, featuring a Spider-Man reference."},{"start_time": 350.639,"end_time": 379.4,"description": "Discussion about the 'relógio de polícia' (police watch) and the stereotypes associated with being a police officer, with humorous banter about physical characteristics and appearance."},{"start_time": 439.36,"end_time": 471.0,"description": "Voting segment where participants discuss and vote on who should be eliminated, with candid comments and a bit of humor about each other's backgrounds and motivations."},{"start_time": 566.44,"end_time": 604.0,"description": "Recreation of a police scenario involving a 'Mike Papa' situation, with humorous confusion and banter about the terminology used."},{"start_time": 706.76,"end_time": 746.199,"description": "Discussion about whether Rodrigo is a police officer, including suspicions about him being armed and having been shot at."},{"start_time": 808.12,"end_time": 848.44,"description": "Simulated police stop with detailed interaction between the officer and the individual being stopped, highlighting procedures and reactions."},{"start_time": 855.32,"end_time": 896.68,"description": "Further exploration of police procedures during a stop, including checking for documents and frisking, with humorous elements."},{'start_time': 1023.199, 'end_time': 1074.44, 'description': 'Interação humorística sobre abordagem policial e comentários engraçados sobre o vídeo.'}, {'start_time': 1111.159, 'end_time': 1158.6, 'description': 'História engraçada sobre interação com a polícia, com humor e reflexões pessoais.'}, {'start_time': 1195.2, 'end_time': 1225.32, 'description': 'Discussão sobre chefes da polícia e situação difícil com troca de tiros, trazendo seriedade e curiosidade.'},{"start_time": 1253.28,"end_time": 1326.84,"description": "Detailed recount of a dangerous shootout and the bravery involved in rescuing a fallen friend."},{"start_time": 1358.72,"end_time": 1432.32,"description": "Humorous segment where participants debate and vote on who is a real police officer, including imitations and funny remarks."},{"start_time": 1452.4,"end_time": 1532.24,"description": "Participants share inspiring stories about impactful moments in their police careers, including rescuing"},{"start_time": 1534.08,"end_time": 1580.44,"description": "Discussion about identifying the real police officer among the participants."},{"start_time": 1608.039,"end_time": 1658.52,"description": "Revealing and discussing the true identity of the real police officer."},{"start_time": 1720.519,"end_time": 1775.76,"description": "Participants reveal their true professions and backgrounds."}]}

    parsed_content = interesting_segment["content"]
    overlay_videos_with_blur(parsed_content, video_id)

    deletar_arquivos(temp_files)
    deletar_arquivos(json_files)
    logging.info('Fim do programa.')