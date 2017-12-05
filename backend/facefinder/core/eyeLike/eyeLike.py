import os
from ctypes import *
import sys


wrapper_path = os.path.dirname(os.path.realpath(__file__))

if os.environ.get('ENV_VAR') == 'prod':
	lib_path = os.path.join(wrapper_path, "build/src/libmylib.so")
else:
	lib_path = os.path.join(wrapper_path, "build/src/libmylib.dylib")

lib = cdll.LoadLibrary(lib_path)
lib.eyes_in_video.restype = c_char_p
lib.eyes_in_video.argtypes = [c_char_p]
lib.eyes_in_picture.restype = c_char_p
lib.eyes_in_picture.argtypes = [c_char_p]

#name = create_string_buffer("/Users/temp/projects/eyeLike/data/sample1.mov")
#s = lib.eyes_in_video(name);
#print_eyes(s)

class Point:
	def __init__(self, x_cord, y_cord):
		if type(x_cord) == str:
			self.x = int(float(x_cord))
		else:
			self.x = x_cord
		if type(y_cord) == str:
			self.y = int(float(y_cord))
		else:
			self.y = y_cord


class Pupils:
	def __init__(self, left_eye, right_eye):
		if type(left_eye) == str:
			self.left = Point(*left_eye.split(','))
		else:
			self.left = left_eye
		if type(right_eye) == str:
			self.right = Point(*right_eye.split(','))
		else:
			self.right = right_eye



def print_eyes(eye_string):
	for i, eyes in enumerate(eye_string.split('F')):
		print("Frame " + str(i+1))
		for eye in eyes.split('/'):
			if len(eye) > 0:
				left, right = eye.split(';')
				print("Left Eye: {0}, Right Eye: {1}".format(left, right))


def parse_eyes(eye_string):
	pupil_list = []
	for i, eyes in enumerate(eye_string.split('F')):
		eyes_in_frame = []
		for eye in eyes.split('/'):
			if len(eye) > 0:
				pupils = Pupils(*eye.split(';'))
				eyes_in_frame.append(pupils)
		pupil_list.append(eyes_in_frame)
	return pupil_list



def get_eye_locations_in_video(full_video_path):
	if sys.version_info.major == 3:
		c_string_path = full_video_path.encode('utf-8')
	else:
		c_string_path = create_string_buffer(full_video_path)
	eye_locations = lib.eyes_in_video(c_string_path)
	return parse_eyes(eye_locations.decode('utf-8'))


def get_eye_locations_in_image(full_image_path):
	if sys.version_info.major == 3:
		c_string_path = full_image_path.encode('utf-8')
	else:
		c_string_path = create_string_buffer(full_image_path)
	eye_location = lib.eyes_in_picture(c_string_path)
	return parse_eyes(eye_location.decode('utf-8'))[0]
