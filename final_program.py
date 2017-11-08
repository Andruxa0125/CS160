import points_68
import video_processor
import sys

path_to_video = './video.mp4'
THREAD_NUM = 4

if (len(sys.argv) == 1):
	print("WARNING: You are using harcoded path to video. Instead, we recommend to pass the path as a parameter.\n\n")
else:
	path_to_video = sys.argv[1]

videoReader  = video_processor.videoReader(path_to_video)
number_of_frames = videoReader.generate_frames()
#print("number of frames is " + str(number_of_frames))
videoReader.create_audio()
step_size = int(number_of_frames / THREAD_NUM)
#print(videoReader.BASE_PICTURE_NAME)
points_68.global_process(videoReader.resulting_folder_path ,videoReader.BASE_PICTURE_NAME,
							videoReader.BASE_PICTURE_EXTENSION, step_size)
videoReader.create_video()