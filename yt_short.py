import cv2
import subprocess
import numpy as np
import math
import logging
import time
from moviepy.editor import VideoFileClip

def enhance_video_quality(input_path, output_path):
    """
    Melhora a qualidade do vídeo aplicando pós-processamento.

    Parâmetros:
    - input_path: Caminho para o vídeo de entrada.
    - output_path: Caminho onde o vídeo processado será salvo.
    """
    command = (
        fr'ffmpeg -i {input_path} -vf '
        fr'eq=contrast=1.5:brightness=0.05:saturation=1.2,unsharp=5:5:1.0:5:5:0.0 '
        fr'-c:a copy {output_path}'
    )
    
    subprocess.call(command, shell=True)
    logging.info(f'Vídeo processado e melhorado salvo em: {output_path}')
    return output_path

def remove_black_borders(video_path, output_path):
    # Carregar o vídeo original
    video = VideoFileClip(video_path)
    
    # Dimensões do vídeo original
    original_width, original_height = video.size

    # Calcular a área sem bordas
    # Esses valores precisam ser ajustados para o seu caso específico
    left = 0  # Ajuste conforme necessário
    top = original_height // 2.8  # Ajuste conforme necessário
    right = original_width  # Ajuste conforme necessário
    bottom = original_height * 2.5 // 4  # Ajuste conforme necessário, diminuir
    
    # Cortar o vídeo
    cropped_video = video.crop(x1=left, y1=top, x2=right, y2=bottom)
    
    # Salvar o vídeo modificado
    cropped_video.write_videofile(output_path, codec="libx264", fps=video.fps)
    return output_path

def segment_video(response, video_id):
    output_files = []
    for i, segment in enumerate(response):
        start_time = math.floor(float(segment.get("start_time", 0)))
        end_time = math.ceil(float(segment.get("end_time", 0))) + 2
        output_file = fr"AIShortsCreator/output/{video_id}_output{str(i).zfill(3)}.mp4"
        input_file = fr"C:\Users\Beffa\Documents\Python\AIShortsCreator\input\{video_id}_input_video.mp4"
        
        # Comando ffmpeg ajustado para aspecto 9:16
        command = (
            fr'ffmpeg -i {input_file} -ss {start_time} -to {end_time} -vf '
            fr'scale=w=1080:h=-1:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2 '
            fr'-c:a copy {output_file}'
        )

        subprocess.call(command, shell=True)
        logging.info(f'Segmento video {i} gerado: {output_file}')
        output_files.append(output_file)
    return output_files

def segment_video_full(response, video_id):
    output_files = []
    for i, segment in enumerate(response):
        start_time = math.floor(float(segment.get("start_time", 0)))
        end_time = math.ceil(float(segment.get("end_time", 0))) + 2
        output_file = fr"AIShortsCreator/output/{video_id}_full_output{str(i).zfill(3)}.mp4"
        input_file = fr"C:\Users\Beffa\Documents\Python\AIShortsCreator\input\{video_id}_input_video.mp4"
        
        # Comando ffmpeg ajustado para preencher a tela toda mantendo a proporção 9:16
        command = (
            fr'ffmpeg -i {input_file} -ss {start_time} -to {end_time} -vf '
            fr'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920 '
            fr'-an -c:v libx264 {output_file}'
        )

        subprocess.call(command, shell=True)
        logging.info(f'Segmento de vídeo {i} gerado: {output_file}')
        output_files.append(output_file)
    return output_files

def overlay_videos_with_blur(response, video_id):
    segmented_videos = segment_video(response, video_id)
    full_segmented_videos = segment_video_full(response, video_id)
    
    for i, (segmented, full_segmented) in enumerate(zip(segmented_videos, full_segmented_videos)):
        output_path = fr"AIShortsCreator/output/{video_id}_final_output{str(i).zfill(3)}.mp4"

        # Remove black borders from segmented video
        time.sleep(2)
        no_border_segmented_path = remove_black_borders(segmented, fr"AIShortsCreator/output/{video_id}_no_border_output{str(i).zfill(3)}.mp4")

        command = (
            fr'ffmpeg -i {no_border_segmented_path} -i {full_segmented} -filter_complex '
            fr'"[1:v]boxblur=luma_radius=60:luma_power=1[blurred];'
            fr'[blurred][0:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" '
            fr'-c:a copy {output_path}'
        )

        subprocess.call(command, shell=True)
        logging.info(f'Vídeo gerado com sobreposição e desfoque: {output_path}')
        
        enhanced_output_path = fr"AIShortsCreator/finalcut/{video_id}_enhanced_output{str(i).zfill(3)}.mp4"
        enhance_video_quality(output_path, enhanced_output_path)



def detect_faces(video_file):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(video_file)
    faces = []
    while len(faces) < 5:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for face in detected_faces:
                if not any(np.array_equal(face, f) for f in faces):
                    faces.append(face)
    cap.release()
    if len(faces) > 0:
        return faces
    return None

def crop_video(faces, input_file, output_file):
    try:
        if len(faces) > 0:
            CROP_RATIO = 0.9  
            VERTICAL_RATIO = 9/16  

            cap = cv2.VideoCapture(input_file)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            target_height = int(frame_height * CROP_RATIO)
            target_width = int(target_height * VERTICAL_RATIO)

            # Create a VideoWriter object to save the output video
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            output_video = cv2.VideoWriter(output_file, fourcc, 30.0, (target_width, target_height))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                for face in faces:
                    x, y, w, h = face

                    crop_x = max(0, x + (w - target_width) // 2)  
                    crop_y = max(0, y + (h - target_height) // 2)
                    crop_x2 = min(crop_x + target_width, frame_width)
                    crop_y2 = min(crop_y + target_height, frame_height)

                    cropped_frame = frame[crop_y:crop_y2, crop_x:crop_x2]
                    resized_frame = cv2.resize(cropped_frame, (target_width, target_height))
                    output_video.write(resized_frame)
            cap.release()
            output_video.release()
            logging.info("Video cropped successfully.")
        else:
            print("No faces detected in the video.")
    except Exception as e:
        print(f"Error during video cropping: {str(e)}")