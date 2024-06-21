# Programa de Criação de Shorts Viral

## Descrição
Este programa tem como objetivo criar vídeos curtos e virais a partir de vídeos do YouTube. Ele realiza automaticamente o download do vídeo, faz os cortes necessários, ajusta o tamanho e gera partes virais, separando-as em vídeos curtos. Além disso, faz todos os ajustes necessários, incluindo a adição de legendas.

## Resultado
- Original
![image](https://github.com/LeonardoBeffa/yt_shorts/assets/171646489/3cbe301c-4db7-41a0-bdb1-127b43b1a07e)
- Final:
![image](https://github.com/LeonardoBeffa/yt_shorts/assets/171646489/946aef12-92cc-4fa1-a321-566a947187fa)

## Funcionalidades

1. **Download de Vídeos do YouTube**: Baixa vídeos diretamente do YouTube para serem processados.
2. **Cortes e Ajustes**: Realiza cortes no vídeo original e ajusta o tamanho para formatos ideais de shorts.
3. **Geração de Prompts de Partes Virais**: Identifica e gera prompts das partes mais virais do vídeo.
4. **Separação em Vídeos Curtos**: Divide o vídeo original em vários vídeos curtos prontos para publicação.
5. **Ajustes Finais e Legendas**: Faz ajustes finais necessários, incluindo a adição de legendas aos vídeos curtos.
6. **Deleta Todos Arquivos Temporarios**: Deleta Todos Arquivos Temporarios utilizados no processo de criação.

## Parte Manual
Atualmente, existe uma pequena parte manual no processo, pois ainda falta a implementação com a IA da OpenAI para tornar o processo totalmente automatizado.

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
- os
- time
- math
- json
- torch
- shutil
- random
- whisper
- logging
- threading
- subprocess
- pytube
- youtube_transcript_api
- moviepy.editor
