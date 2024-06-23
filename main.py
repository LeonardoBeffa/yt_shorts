from yt_video_transcript import get_transcript, download_video
from yt_short import executavel
import os
import logging
import json

os.system('cls')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

video_id = '2lSHKP8eMmc' #ID do video. 
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

def prompt_generator(transcript, video_id):
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
    
    if not os.path.exists(fr'{relative_path}\prompts\{video_id}.json'):
        with open(fr'{relative_path}\prompts\{video_id}.json', 'w', encoding='utf-8') as file:
            for i in range(1, ((len(dic_temp))+1)):
                file.write(f'\nPrompt {i}\n')
                file.write('You are a ViralGPT helpful assistant. You are master at reading youtube transcripts and identifying the most Interesting and Viral Content\n')
                file.write(f"This is a transcript of a video. Please identify the 3 most viral sections from the whole, make sure they are more than 40 seconds in duration, Make Sure you provide extremely accurate timestamps respond only in this format {template}. json, Here is the Transcription:\n")
                file.write(json.dumps(dic_temp[f'content{i}'], indent=4, ensure_ascii=False))
                file.write('\n')
            logging.info(f'Prompts Gerados. Total: {i} de 6')
    else:
        logging.info(f'Prompts Existente. {video_id}')

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
verifica_ou_cria_pasta(fr'{relative_path}\prompts')
verifica_ou_cria_pasta(temp_files)
verifica_ou_cria_pasta(json_files)

#Alterar aqui para pegar os cortes. (alt + z), por padrao fica em None, coloque o prompt gerado.
interesting_segment = {'content': [{'start_time': 70.6, 'end_time': 122.52, 'description': 'Introdução dos participantes, com destaque para as profissões e comentários humorísticos sobre a situação.'},{"start_time": 135.72,"end_time": 175.72,"description": "Johnny falando sobre sua adolescência e a pomadinha da vó."},{"start_time": 203.159,"end_time": 246.56,"description": "Vinícius discute suas experiências como garçom e os desafios com o uniforme."},{'start_time': 144.0, 'end_time': 195.799, 'description': 'História do Vitor sobre seu sonho de ser jogador de futebol, o uso de GH e a condição de bromidrose, incluindo apelidos e a música cantada por colegas.'},{"start_time": 187.519,"end_time": 234.159,"description": "Vittor fala sobre sua infância, tratamento para crescimento e bromidrose."},{'start_time': 216.319, 'end_time': 282.52, 'description': 'Relato do Milton sobre sua experiência com CC desde a infância, uso de pomada, desenvolvimento de alergia e situações engraçadas associadas.'},{"start_time": 393.36,"end_time": 442.36,"description": "Discussion about Botox and electroshock treatments for excessive sweating, with humorous exchanges about the effects and the transfer of odor to other parts of the body."},{"start_time": 477.68,"end_time": 527.6,"description": "Exploration of hyperosmia (heightened sense of smell) and its impact on daily life and work, including dealing with strong odors in a kitchen environment."},{"start_time": 600.44,"end_time": 652.92,"description": "Conversation about how people notice and react to body odor, with personal anecdotes about how others' reactions can signal the presence of an unpleasant smell."},{"start_time": 724.959,"end_time": 764.16,"description": "Discussion about the guest's relationship, infidelity, and the reactions to his hygiene."},{"start_time": 907.12,"end_time": 950.72,"description": "Conversation about personal hygiene and working conditions in a kitchen, including humorous exchanges about smell and cleanliness."},{"start_time": 974.399,"end_time": 1017.199,"description": "Detailed discussion on daily routines, hygiene practices, and the challenges faced in maintaining cleanliness in a busy lifestyle."},{"start_time": 1231.88,"end_time": 1261.0,"description": "Discussion about the experience of riding a crowded bus and dealing with unpleasant odors, leading to a humorous exchange about taking a shower before the ride."},{"start_time": 1303.76,"end_time": 1345.039,"description": "A funny story about working as a shop salesman and dealing with body odor, which affected his sales performance, followed by reactions from others."},{"start_time": 1375.48,"end_time": 1404.96,"description": "A comedic segment involving a challenge to smell someones armpit to verify body odor, with humorous commentary and reactions from the participants."},{'start_time': 1487.559,'end_time': 1531.32,'description': 'Humorous and intense moment with participants discussing and experiencing unpleasant smells, leading to laughter and reactions.'},{'start_time': 1553.08,'end_time': 1607.72,'description': 'Engaging discussion about the social consequences of bad odor, including personal anecdotes and humorous exchanges.'},{'start_time': 1643.52,'end_time': 1709.24,'description': 'Debate about whether bad odor is real or a character act, with funny and insightful commentary on the nature of body odor.'},{'start_time': 1910.48, 'end_time': 1936.48, 'description': 'Vitor reveals that he is a chef and restaurant owner, explaining his experience with bathing to remove kitchen grease.'}, {'start_time': 2001.2, 'end_time': 2029.679, 'description': 'Discussion about personal hygiene and the exaggeration of body odor issues, involving humorous and relatable anecdotes.'}, {'start_time': 2072.639, 'end_time': 2101.56, 'description': 'Introduction of a personal hygiene kit, featuring various products and a humorous demonstration.'}]}

if interesting_segment == None:
    download_video(input_path, video_id)
    transcript = get_transcript(video_id)
    prompt_generator(transcript, video_id)
    logging.info('Fim do programa.')
else:
    parsed_content = interesting_segment["content"]
    executavel(video_id, parsed_content)

    deletar_arquivos(temp_files)
    deletar_arquivos(json_files)
    logging.info('Fim do programa.')