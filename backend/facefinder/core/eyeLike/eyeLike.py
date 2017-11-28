import os
from ctypes import *

wrapper_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(wrapper_path, "build/src/libmylib.dylib")

lib = cdll.LoadLibrary(lib_path)
lib.eyes_in_video.restype = c_char_p
lib.eyes_in_video.argtypes = [c_char_p]
lib.eyes_in_picture.restype = c_char_p
lib.eyes_in_picture.argtypes = [c_char_p]

#name = create_string_buffer("/Users/temp/projects/eyeLike/data/sample1.mov")
#s = lib.eyes_in_video(name);
#print_eyes(s)


def print_eyes(eye_string):
	for i, eyes in enumerate(eye_string.split('F')):
		for eye in eyes.split('/'):
			if len(eye) > 0:
				print eye
		print "Frame " + str(i+1)


def get_eye_locations_in_video(full_video_path):
	c_string_path = create_string_buffer(full_video_path)
	eye_locations = lib.eyes_in_video(c_string_path)
	return eye_locations


def get_eye_locations_in_image(full_image_path):
	c_string_path = create_string_buffer(full_image_path)
	eye_location = lib.eyes_in_picture(c_string_path)
	return eye_location