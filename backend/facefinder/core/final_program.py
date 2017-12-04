from . import points_68
from . import video_processor
import sys
import multiprocessing
import os

path = '/home/andrey/video.mp4'
THREAD_NUM = 4


def run_video(path_to_video, video=None):
    videoReader = video_processor.videoReader(path_to_video)
    number_of_frames, height, width, frame_rate = videoReader.generate_frames()
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
    if os.environ.get('ENV_VAR') == 'dev':
        multiprocessing.set_start_method('spawn')
    points_68.global_process(videoReader.resulting_folder_path ,videoReader.BASE_PICTURE_NAME,
    							videoReader.BASE_PICTURE_EXTENSION, step_size)
    videoReader.create_video()

if __name__ == "__main__":
    run_video(path)

