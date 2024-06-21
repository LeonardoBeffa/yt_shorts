from yt_video_transcript import get_transcript, download_video
from yt_short import overlay_videos_with_blur
import os
import logging

os.system('cls')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

video_id = 't0bdqJrVJdk' #ID do video. Somente alterar aqui
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
        print('You are a ViralGPT helpful assistant. You are master at reading youtube transcripts and identifying the most Interesting and Viral Content\n')
        print(f"This is a transcript of a video. Please identify the 3 most viral sections from the whole, make sure they are more than 40 seconds in duration, Make Sure you provide extremely accurate timestamps respond only in this format {template}. json, Here is the Transcription:\n")
        print(dic_temp[f'content{i}'])
        print()
    logging.info(f'Prompts Gerados. {i} de 6')

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

cond = 1
if cond == 0:
    download_video(input_path, video_id)
    transcript = get_transcript(video_id)
    prompt_generator(transcript)
    logging.info('Fim do programa.')
else:
    #Alterar aqui para pegar os cortes. (alt + z)
    interesting_segment = {'content': [{'start_time': 0.12, 'end_time': 54.28, 'description': 'Introduction to the video and its concept, explaining the rules and the competition with a surprise for the participants.'}, {'start_time': 63.16, 'end_time': 136.84, 'description': 'Round one where participants are ranked based on appearance, with humorous and engaging interactions among the hosts.'}, {'start_time': 170.44, 'end_time': 276.919, 'description': 'Round two, where the hosts ask the participants about their areas of work and favorite restaurants, leading to interesting and funny responses.'},{"start_time": 318.32,"end_time": 379.72,"description": "Discussion about international travels, frequency of trips, and associated costs, featuring some humor and curiosity about destinations."},{"start_time": 471.84,"end_time": 526.88,"description": "Conversation about meeting Mickey at Disney, including personal emotions and reactions, transitioning into questions about household appliances with humorous elements."},{"start_time": 536.68,"end_time": 598.24,"description": "Light-hearted banter about refrigerators, the number of doors they have, and a humorous debate on the truthfulness of these claims, ending with a discussion on hobbies like football and samba."},{'start_time': 600.16, 'end_time': 641.639, 'description': 'Humorous exchange about perceptions and reactions to a montage and interactions among friends.'}, {'start_time': 688.399, 'end_time': 729.079, 'description': 'Discussion about travel expenses, affordable prices, and gratitude for last-minute deals.'}, {'start_time': 740.12, 'end_time': 780.12, 'description': 'Rapid-fire questions about financial status, personal preferences, and social habits.'},{"start_time": 969.04,"end_time": 996.399,"description": "O Léo fala sobre ser o menos abastado financeiramente e a discussão segue sobre o impacto disso no grupo."},{"start_time": 1030.36,"end_time": 1055.24,"description": "Os participantes discutem os itens mais caros que já compraram, incluindo um PC de 4000 e a obra de uma cozinha."},{"start_time": 1087.039,"end_time": 1121.039,"description": "Paloma fala sobre os itens caros que já comprou, como um iPad e um grill de dente de ouro, gerando reações surpreendidas dos outros participantes."},{'start_time': 1263.64, 'end_time': 1302.08, 'description': 'Discussion on the possibility of Gustavo earning more and the challenges of interpreting peoples financial situations.'}, {'start_time': 1343.6, 'end_time': 1394.24, 'description': 'Analysis of the potential cost of travel destinations and the expenses related to personal property improvements.'}, {'start_time': 1398.4, 'end_time': 1425.88, 'description': 'Final debate on the rankings of individuals based on perceived financial status, with a focus on Gustavo and Tulio.'},{"start_time": 1536.279,"end_time": 1572.48,"description": "Excitement and tension build as the group waits for the results of a competition, leading to a moment of celebration and relief."},{"start_time": 1643.279,"end_time": 1672.279,"description": "The group celebrates their victory and everyone is awarded R$3,000 for travel packages, creating a joyful and triumphant atmosphere."},{"start_time": 1692.2,"end_time": 1710.039,"description": "The conversation turns lively with discussions about relationships, ending with a call to action for viewers to like, subscribe, and comment."}]}

    parsed_content = interesting_segment["content"]
    overlay_videos_with_blur(parsed_content, video_id)

    deletar_arquivos(temp_files)
    deletar_arquivos(json_files)
    logging.info('Fim do programa.')