# import video_processor as video_processor
# import points_68
from . import points_68
from . import video_processor
import sys
import multiprocessing
import os
import json
from backend.settings import BASE_DIR

path = '/home/andrey/video.mp4'
THREAD_NUM = 4


def run_video(path_to_video, video=None):
    videoReader = video_processor.videoReader(path_to_video)
    number_of_frames, height, width, frame_rate = videoReader.generate_frames()
    #django stuff
    if video:
        video.video_number_of_frames = number_of_frames
        video.video_height = height
        video.video_width = width
        video.video_frame_rate = frame_rate
        video.save()

    #print("number of frames is " + str(number_of_frames))
    videoReader.create_audio()
    step_size = int(number_of_frames / THREAD_NUM)
    #print(videoReader.BASE_PICTURE_NAME)
    # if os.environ.get('ENV_VAR') == 'dev':
    #     multiprocessing.set_start_method('spawn')
    points_68.global_process(videoReader.resulting_folder_path ,videoReader.BASE_PICTURE_NAME,
    							videoReader.BASE_PICTURE_EXTENSION, step_size)
    yaw_pitch_roll = json.load(open(BASE_DIR + '/media/documents/RESULTS_FOLDER_NAME/data.json'))
    video.video_roll_pitch_yaw = yaw_pitch_roll
    video.save()
    videoReader.create_video()

    # with open("/home/andrey/RESULTS_FOLDER_NAME/points.json") as f1:
    #     data = json.load(f1)
    # print("length is " + str(len(data)))
    # print("length is " + str(len(data["1"])))

if __name__ == "__main__":
    run_video(path)


