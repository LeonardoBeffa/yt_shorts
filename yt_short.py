import cv2
import subprocess
import numpy as np
import math
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#Segment Video function
def segment_video(response, video_id):
    for i, segment in enumerate(response):
        start_time = math.floor(float(segment.get("start_time", 0)))
        end_time = math.ceil(float(segment.get("end_time", 0))) + 2
        output_file = fr"AI-Shorts-Creator-main/output/{video_id}_output{str(i).zfill(3)}.mp4"
        command = fr"ffmpeg -i C:\Users\Beffa\Documents\Python\AI-Shorts-Creator-main\input\{video_id}_input_video.mp4 -ss {start_time} -to {end_time} -c copy {output_file}"
        subprocess.call(command, shell=True)
        logging.info('Segmento video.')

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
            VERTICAL_RATIO = 9 / 16  

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