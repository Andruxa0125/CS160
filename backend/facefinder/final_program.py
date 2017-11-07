from . import points_68
from . import video_processor

def run_video(path):
	path_to_video = path
	THREAD_NUM = 4

	videoReader = video_processor.videoReader(path_to_video)
	number_of_frames = videoReader.generate_frames()
	videoReader.create_audio()
	number_of_frames = 900
	step_size = int(number_of_frames / THREAD_NUM)
	print(videoReader.BASE_PICTURE_NAME)
	points_68.global_process(videoReader.resulting_folder_path ,videoReader.BASE_PICTURE_NAME,
								videoReader.BASE_PICTURE_EXTENSION, step_size)
	videoReader.create_video()

#def global_process(self, path_to_pics, base_name, extension, step_size): 