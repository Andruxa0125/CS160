#import video_processor as video_processor
#import points_68
from . import points_68
from . import video_processor
import sys
<<<<<<< 644ebe658c697dd1bb5d99f751821aacc7941fe6
import multiprocessing
=======
import json
>>>>>>> added roll, pitch, yaw and json with all frames

path = '/home/andrey/video.mp4'
THREAD_NUM = 4


def run_video(path_to_video, video=None):
    videoReader  = video_processor.videoReader(path_to_video)
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
    multiprocessing.set_start_method('spawn')
    points_68.global_process(videoReader.resulting_folder_path ,videoReader.BASE_PICTURE_NAME,
    							videoReader.BASE_PICTURE_EXTENSION, step_size)
    videoReader.create_video()
    # data = json.load(open('/home/andrey/RESULTS_FOLDER_NAME/data.json'))
    # print(len(data))

if __name__ == "__main__":
    run_video(path)

