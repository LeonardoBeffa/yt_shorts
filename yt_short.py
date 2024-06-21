import subprocess
import math
import logging
import time
from moviepy.editor import VideoFileClip
from yt_pngs import add_watermark, add_text
from yt_subtitle import subtitle
import os
import shutil

path = fr'AIShortsCreator/output'
input_path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator\input'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()

def render_video_quality(input_path, output_path):
    command = (
        f'ffmpeg -i {input_path} -vf '
        f'eq=contrast=1.2:brightness=0.05:saturation=1,unsharp=5:5:1.0:5:5:0.0 '
        f'-c:v h264_nvenc -preset fast -c:a copy {output_path}'
    )
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f'Vídeo processado e salvo em: {output_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Erro ao processar vídeo: {e}')
    return output_path

def remove_black_borders(video_path, output_path):
    video = VideoFileClip(video_path)
    original_width, original_height = video.size

    left = 0  
    top = original_height // 2.9  
    right = original_width  
    bottom = original_height * 2.6 // 4 #melhor config - 2.6

    cropped_video = video.crop(x1=left, y1=top, x2=right, y2=bottom)
    cropped_video.write_videofile(output_path, codec="libx264", fps=video.fps)
    return output_path

def segment_video(response, video_id):
        output_files_normal = []
        output_files_full = []

        for i, segment in enumerate(response):
            
            start_time = math.floor(float(segment.get("start_time", 0)))
            end_time = math.ceil(float(segment.get("end_time", 0))) + 1
            real_time =  end_time - start_time

            if real_time <= int(61):
                input_file = fr"{input_path}\{video_id}_input_video.mp4"
                output_file_normal = fr"{path}/{video_id}_output{str(i).zfill(3)}.mp4"
                output_file_full = fr"{path}/{video_id}_full_output{str(i).zfill(3)}.mp4"
                
                command_normal = (
                    fr'ffmpeg -i {input_file} -ss {start_time} -to {end_time} -vf '
                    fr'scale=w=1080:h=-1:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2 '
                    fr'-c:v h264_nvenc -preset fast -c:a copy {output_file_normal}'
                )

                subprocess.run(command_normal, shell=True, check=True)
                logging.info(f'Segmento video {i} gerado: {output_file_normal}')

                command_full = (
                    fr'ffmpeg -i {input_file} -ss {start_time} -to {end_time} -vf '
                    fr'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920 '
                    fr'-c:v h264_nvenc -preset fast -c:a copy {output_file_full}'
                )

                subprocess.run(command_full, shell=True, check=True)
                logging.info(f'Segmento video {i} gerado: {output_file_full}')

                output_files_normal.append(output_file_normal)
                output_files_full.append(output_file_full)
            
                return output_files_normal, output_files_full
            else:
                pass


def overlay_videos_with_blur(response, video_id):

    segmented_videos, full_segmented_videos = segment_video(response, video_id)

    for i, (segmented, full_segmented) in enumerate(zip(segmented_videos, full_segmented_videos)):
        output_path = fr"{path}/{video_id}_final_output{str(i).zfill(3)}.mp4"

        time.sleep(2)
        no_border_segmented_path = remove_black_borders(segmented, fr"{path}/{video_id}_no_border_output{str(i).zfill(3)}.mp4")

        command = (
            fr'ffmpeg -i {no_border_segmented_path} -i {full_segmented} -filter_complex '
            fr'"[1:v]boxblur=luma_radius=60:luma_power=1[blurred];'
            fr'[blurred][0:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" '
            fr'-c:v h264_nvenc -preset fast -c:a copy {output_path}'
        )

        subprocess.run(command, shell=True, check=True)
        logging.info(f'Vídeo gerado com sobreposição e desfoque: {output_path}')
        
        render_output_path = fr"{path}/{video_id}_posprocess_output{str(i).zfill(3)}.mp4"
        render_video_quality(output_path, render_output_path)
        
        watermark_output_path = fr"{path}/{video_id}_watermark_output{str(i).zfill(3)}.mp4"
        add_watermark(render_output_path,watermark_output_path)
        
        text_output_path = fr"{path}/{video_id}_text_{str(i).zfill(3)}.mp4"
        add_text(watermark_output_path, text_output_path)
        
        final_output_path = fr"AIShortsCreator/final/{video_id}_final_{str(i).zfill(3)}.mp4"
        subtitle(text_output_path, final_output_path, video_id, i)
