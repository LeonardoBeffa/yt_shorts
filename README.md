# Programa de Criação de Shorts Viral

## Descrição
Este programa tem como objetivo criar vídeos curtos e virais a partir de vídeos do YouTube. Ele realiza automaticamente o download do vídeo, faz os cortes necessários, ajusta o tamanho e gera partes virais, separando-as em vídeos curtos. Além disso, faz todos os ajustes necessários, incluindo a adição de legendas.

## Funcionalidades

1. **Download de Vídeos do YouTube**: Baixa vídeos diretamente do YouTube para serem processados.
2. **Cortes e Ajustes**: Realiza cortes no vídeo original e ajusta o tamanho para formatos ideais de shorts.
3. **Geração de Prompts de Partes Virais**: Identifica e gera prompts das partes mais virais do vídeo.
4. **Separação em Vídeos Curtos**: Divide o vídeo original em vários vídeos curtos prontos para publicação.
5. **Ajustes Finais e Legendas**: Faz ajustes finais necessários, incluindo a adição de legendas aos vídeos curtos.

## Parte Manual
Atualmente, existe uma pequena parte manual no processo, pois ainda falta a implementação com a IA da OpenAI para tornar o processo totalmente automatizado.

## Estrutura do Projeto

viral-shorts-creator/
│
├── download_video.py # Script para baixar vídeos do YouTube
├── cut_and_resize.py # Script para realizar cortes e ajustes de tamanho
├── generate_prompts.py # Script para gerar prompts de partes virais
├── separate_videos.py # Script para separar vídeos em partes curtas
├── add_captions.py # Script para adicionar legendas aos vídeos curtos
├── main.py # Script principal para orquestrar todo o processo
│
├── utils/
│ ├── video_downloader.py # Módulo para baixar vídeos
│ ├── video_editor.py # Módulo para edição de vídeos
│ ├── prompt_generator.py # Módulo para geração de prompts virais
│ ├── video_splitter.py # Módulo para separar vídeos em partes curtas
│ └── caption_adder.py # Módulo para adicionar legendas
│
├── data/
│ ├── raw_videos/ # Pasta para armazenar vídeos baixados
│ ├── edited_videos/ # Pasta para armazenar vídeos editados
│ └── short_videos/ # Pasta para armazenar vídeos curtos finais
│
├── README.md # Documentação do projeto
└── requirements.txt # Dependências do projeto

## Uso
Para utilizar este programa, siga os passos abaixo:

1. **Adicionar o ID do vídeo**
   - Identifique o ID do vídeo que deseja analisar.
   - Exemplo de um ID de vídeo do YouTube: `dQw4w9WgXcQ`.
   - Insira este ID no campo apropriado do programa.

2. **Utilizar os prompts gerados para descobrir as partes virais do vídeo**
   - O programa irá gerar uma série de prompts que ajudarão a identificar as partes mais populares ou virais do vídeo.

3. **Adicionar ao programa**
   - Utilize as informações dos prompts gerados e adicione-as ao programa conforme as instruções fornecidas.

4. **Esperar o programa executar**
   - Inicie a execução do programa.
   - Espere até que o programa conclua a execução e forneça os resultados.

### Pré-requisitos
- Python 3.x
- Bibliotecas listadas em `requirements.txt
