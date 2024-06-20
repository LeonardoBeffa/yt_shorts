from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import logging
import os

#Para o arquivo yt_pngs funcionar é necessario criar uma pasta PNGS
#E adicionar os arquivos relevantas.
#Edit o path com o caminho até a pasta.

path = fr'C:\Users\Beffa\Documents\Python\AIShortsCreator'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
os.system('cls')

def add_png_in_clip(video_path, output_path, png_path,position,opacity,png_scale):  
    video = VideoFileClip(video_path)
    
    imag_png = ImageClip(png_path, transparent=True).set_duration(video.duration)
    imag_png = imag_png.resize(png_scale)
    imag_png = imag_png.set_opacity(opacity)

    if position[0] == "left":
        x_pos = 0
    elif position[0] == "center":
        x_pos = (video.w - imag_png.w) / 2
    elif position[0] == "right":
        x_pos = video.w - imag_png.w

    if position[1] == "top":
        y_pos = 0
    elif position[1] == "center":
        y_pos = (video.h - imag_png.h) / 2
    elif position[1] == "bottom":
        y_pos = video.h - imag_png.h

    imag_png = imag_png.set_position((x_pos, y_pos))
    final_clip = CompositeVideoClip([video, imag_png])
    final_clip.write_videofile(output_path, codec='libx264', ffmpeg_params=['-c:v', 'h264_nvenc', '-preset', 'fast'])
    logging.info(f'Finalizando PNG em {video_path}')

def add_watermark(input_path, output_path):
    png_path_watermark = fr"{path}\pngs\watermark.png"
    position = ("right", "bottom") 
    opacity = 0.6  
    png_scale = 0.5
    logging.info('Adicionando Watermark.')
    add_png_in_clip(input_path, output_path, png_path_watermark, position, opacity, png_scale)

def add_text(input_path, output_path):
    png_path_text = fr"{path}\pngs\inscr.png"
    position = ("center", "bottom") 
    opacity = 0.9  
    png_scale = 2
    logging.info('Adicionando Texto...')
    add_png_in_clip(input_path, output_path, png_path_text, position, opacity, png_scale)
