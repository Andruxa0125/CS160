import execute
import re
import os
import shutil
import sys
import glob
#https://stackoverflow.com/questions/9913032/ffmpeg-to-extract-audio-from-video
#ffmpeg -r 20.0 -start_number 1 -f image2 -i "pic%d.png" -vcodec mjpeg -i sample.mp3 -qscale 1 attempt.avi
# get audio from video ffmpeg -i input-video.avi -vn -acodec copy output-audio.aac

class videoReader():

    #GLOBAL CONSTANTS
    RESULTS_FOLDER_NAME = "RESULTS_FOLDER_NAME"
    BASE_PICTURE_NAME = "pic"
    AUDIO_VIDEO_NAME = "result"
    DEFAULT_AUDIO_EXTENSION = ".mp3"
    BASE_PICTURE_EXTENSION = "jpg"

    #COMMANDS THAT WILL BE ISSUED
    FRAME_RATE_COMMAND = ("ffprobe -v error -select_streams v:0 " \
                         "-show_entries stream=avg_frame_rate " \
                         "-of default=noprint_wrappers=1:nokey=1 ")
    EXTRACT_COMMAND = ("ffmpeg -i %s -vf fps=%s %s%%d.jpg")
    #CREATE_VIDEO_COMMAND = ('ffmpeg -r %s -start_number 1 -f image2 -i "%s%%d.jpg" -i %s -vcodec mjpeg -qscale 1 %s.avi')
    CREATE_VIDEO_COMMAND = ('ffmpeg -f image2 -loop 1 -r %s -i %s%%d.jpg -i %s -shortest -c:a copy -c:v libx264 -crf 23 -preset veryfast %s.mp4')
    CREATE_AUDIO_COMMAND = ('ffmpeg -i %s -q:a 0 -map a %s%s')

    #REGEX NEEDED TO GET FRAME RATE AS DOUBLE
    REGEX_FRAME_RATE = "(\d+)/(\d+)"

    def __init__(self, path_to_video):
        """
        After initializing videoReader object, path to the video will
        be saved and all function will operate on that path.
        The path to the video has to be either absolute or relative.
        """
        # if(not os.path.isfile(path_to_video)):
        #     raise Exception("The path to the video doesn't exist")
        self.path_to_video = path_to_video
        self.frame_rate = -1
        absolute_path_to_video = os.path.abspath(path_to_video) #get absolute path to video
        if not os.path.isfile(absolute_path_to_video):
            print("Couldn't locate the the file. If you are passing as parameter, make sure the path is valid. Otherwise, check the code for hardcoded path.")
            sys.exit("\nWe have to finish.")
        absolute_folder_of_video = os.path.dirname(absolute_path_to_video) #absolute path to folder containing video
        # resulting absolute path
        self.resulting_folder_path = os.path.join(absolute_folder_of_video, videoReader.RESULTS_FOLDER_NAME)
        
        if(os.path.isdir(self.resulting_folder_path)):
            print("Removing folder %s" % self.resulting_folder_path)
            shutil.rmtree(self.resulting_folder_path)
        print("Creating folder %s\n" % self.resulting_folder_path)
        os.makedirs(self.resulting_folder_path)
        
    def create_audio(self):
        """
        Based on the path to video, an audio track with name 
        AUDIO_VIDEO_NAME.mp3 will be created in folder 
        ./RESULTS_FOLDER_NAME
        """
        audio_dir = os.path.join(self.resulting_folder_path, videoReader.AUDIO_VIDEO_NAME)
        cmd = videoReader.CREATE_AUDIO_COMMAND % (self.path_to_video, audio_dir,
                                                  videoReader.DEFAULT_AUDIO_EXTENSION)
        print("Issuing following command to create audio:\n" + cmd + "\n")
        command = execute.command()
        command.execute(cmd)

    def create_video(self):
        """
        This function will look for frames in following directory
        self.path_to_video/result_folder.
        It will look for pictures with the following format
        BASE_PICTURE_NAME%d.png
        """
        frames_dir = os.path.join(self.resulting_folder_path, videoReader.BASE_PICTURE_NAME)
        video_dir = os.path.join(self.resulting_folder_path, videoReader.AUDIO_VIDEO_NAME)
        audio_file_name = videoReader.AUDIO_VIDEO_NAME + videoReader.DEFAULT_AUDIO_EXTENSION
        audio_file_path = os.path.join(self.resulting_folder_path, audio_file_name)
        cmd = videoReader.CREATE_VIDEO_COMMAND % (self.frame_rate, frames_dir,
                                                audio_file_path, video_dir)
        print("Issuing following command to create video:\n" + cmd + "\n")
        command = execute.command()
        command.execute(cmd)
        self.clean_up()

    def generate_frames(self):
        """
        Based on the path to video, this function will create
        frames with the following names 
        BASE_PICTURE_NAME%d.png in folder ./RESULTS_FOLDER_NAME
        returns the number of generates frames.
        """
        self.frame_rate = self.get_frame_rate(self.path_to_video)
        frame_dir = os.path.join(self.resulting_folder_path, videoReader.BASE_PICTURE_NAME)
        cmd = videoReader.EXTRACT_COMMAND % (self.path_to_video, self.frame_rate,
                                            frame_dir)
        print("Issuing following command generate frames:\n" + cmd + "\n")
        command = execute.command()
        command.execute(cmd)
        return len(glob.glob1(self.resulting_folder_path,"*.%s" % videoReader.BASE_PICTURE_EXTENSION))


    def get_frame_rate(self, path_to_video):
        """
        This is a helper function that based on the class variable
        self.path_to_video will issue a command to get the frame rate
        in a format of a string "30/4".
        It will call a helper function that will get a float result.
        Returns: frame rate as a float
        """
        cmd = videoReader.FRAME_RATE_COMMAND + path_to_video
        command = execute.command()
        result = command.execute(cmd)
        #bytes to string
        result = result.decode('ascii')
        result = self.process_frame_rate_str(result)
        return result

    def process_frame_rate_str(self, frame_rate_str):
        """
        This function takes a frame rate as a string "30/4" and
        returns an actual float.
        Returns: "30/4" as a float.
        """
        matcher = re.match(videoReader.REGEX_FRAME_RATE, frame_rate_str,
                                                                flags=0)
        result = "No match"
        if(matcher):
            num1 = int(matcher.group(1))
            num2 = int(matcher.group(2))
            result = num1 / num2
            result = float("{0:.2f}".format(result))
        return result

    def clean_up(self):
        """
        deletes all the files that are not video.
        """
        folder = self.resulting_folder_path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if (os.path.isfile(file_path) and not file_path.endswith('.mp4')):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    path_to_video = ''
    if(len(sys.argv) == 1):
        raise Exception("The program needs path to the video")
    else:
        path_to_video = sys.argv[1]

    videoReader  = videoReader(path_to_video)
    frames_number = videoReader.generate_frames()
    videoReader.create_audio()

    videoReader.create_video()