import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import whisper
import json
import torch
import random
import logging
import threading

json_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\json'
pngs_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\pngs'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
os.system('cls')

def audio_extrac(videofilename, audiofilename):
    try:
        video_clip = VideoFileClip(videofilename)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audiofilename)
        logging.info(f"Arquivo de áudio salvo em: {audiofilename}")
        return audiofilename
    except Exception as e:
        print(f"Erro ao extrair áudio: {e}")

def ft_whisper(audiofilename):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = whisper.load_model('large', device=device)
    try:
        segments = model.transcribe(audiofilename, word_timestamps=True)["segments"]
        return segments
    except ValueError as e:
        print(f"Erro: {e}")

def split_text_into_lines(data):
    MaxChars = 30
    MaxDuration = 2.5
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0

    for idx, word_data in enumerate(data):
        word = word_data['word']
        start = word_data['start']
        end = word_data['end']

        line.append({
            "word": word,
            "start": start,
            "end": end
        })
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)
        new_line_chars = len(temp)

        if idx > 0:
            gap = start - data[idx - 1]['end']
            maxgap_exceeded = gap > MaxGap
        else:
            maxgap_exceeded = False

        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars

        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0

    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles

def get_word_size(word, font, fontsize):
    word_clip = TextClip(word, font=font, fontsize=fontsize, color='white')
    return word_clip.size

def get_random_color():
    colors = ['yellow']
    return random.choice(colors)

def create_caption(textJSON, framesize, color='white', stroke_color='black', stroke_width=1.5):
    font = fr"{pngs_path}\Helvetica.ttf"
    full_duration = textJSON['end'] - textJSON['start']
    
    word_clips = []
    xy_textclips_positions = []

    x_pos = y_pos = line_width = 0
    frame_width = framesize[0]
    frame_height = framesize[1]
    x_buffer = frame_width * 1 / 10
    max_line_width = frame_width - 2 * (x_buffer)
    fontsize = int(frame_height * 0.052)  #FonteSize.

    space_width = ""
    space_height = ""

    for index, wordJSON in enumerate(textJSON['textcontents']):
        duration = wordJSON['end'] - wordJSON['start']
        word_clip = TextClip(wordJSON['word'], font=font, fontsize=fontsize, color=color, stroke_color=stroke_color, stroke_width=stroke_width).set_start(textJSON['start']).set_duration(full_duration)
        word_clip_space = TextClip(" ", font=font, fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)

        word_width, word_height = get_word_size(wordJSON['word'], font, fontsize)
        space_width, space_height = get_word_size(" ", font, fontsize)

        if line_width + word_width + space_width <= max_line_width:
            highlight_color = get_random_color()

            xy_textclips_positions.append({
                "x_pos": x_pos,
                "y_pos": y_pos,
                "width": word_width,
                "height": word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration,
                "highlight_color": highlight_color
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos + word_width, y_pos))

            x_pos += word_width + space_width
            line_width += word_width + space_width

        else:
            x_pos = 0
            y_pos = y_pos + word_height + 6
            line_width = word_width + space_width

            highlight_color = get_random_color()

            xy_textclips_positions.append({
                "x_pos": x_pos,
                "y_pos": y_pos,
                "width": word_width,
                "height": word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration,
                "highlight_color": highlight_color
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos + word_width, y_pos))

            x_pos = x_pos + word_width + space_width

        word_clips.append(word_clip)
        word_clips.append(word_clip_space)

    for highlight_word in xy_textclips_positions:
        word_clip_highlight = TextClip(highlight_word['word'], font=font, fontsize=fontsize, color=highlight_word['highlight_color'], stroke_color=stroke_color, stroke_width=stroke_width).set_start(highlight_word['start']).set_duration(highlight_word['duration']).set_position((highlight_word['x_pos'], highlight_word['y_pos']))
        word_clips.append(word_clip_highlight)

    return word_clips, xy_textclips_positions

def subtitle(videofilename, output_path, video_id, idx):
    audiofilename = videofilename.replace(".mp4", '.mp3')
    audio_thread = threading.Thread(target=audio_extrac, args=(videofilename, audiofilename))
    audio_thread.start()
    audio_thread.join()

    segments = ft_whisper(audiofilename)

    wordlevel_info = [{'word': word["word"], 'start': word["start"], 'end': word["end"]} for segment in segments for word in segment["words"]]
    with open(fr'{json_path}\{video_id}_data_{str(idx).zfill(3)}.json', 'w', encoding='utf-8') as f:
        json.dump(wordlevel_info, f, indent=4, ensure_ascii=False)

    linelevel_subtitles = split_text_into_lines(wordlevel_info)

    input_video = VideoFileClip(videofilename)
    frame_size = input_video.size

    all_linelevel_splits = []

    for line in linelevel_subtitles:
        out_clips, positions = create_caption(line, frame_size)

        max_width = 0
        max_height = 0

        for position in positions:
            x_pos, y_pos = position['x_pos'], position['y_pos']
            width, height = position['width'], position['height']

            max_width = max(max_width, x_pos + width)
            max_height = max(max_height, y_pos + height)

        color_clip = ColorClip(size=(int(max_width * 1.1), int(max_height * 1.1)), color=(64, 64, 64))
        color_clip = color_clip.set_opacity(0)
        color_clip = color_clip.set_start(line['start']).set_duration(line['end'] - line['start'])
        
        clip_to_overlay = CompositeVideoClip([color_clip] + out_clips)

        clip_to_overlay = clip_to_overlay.set_position(lambda t:("center",70+t))

        all_linelevel_splits.append(clip_to_overlay)

    final_video = CompositeVideoClip([input_video] + all_linelevel_splits).set_audio(input_video.audio)
    final_video.write_videofile(output_path, fps=input_video.fps, codec="libx264", audio_codec="aac")
