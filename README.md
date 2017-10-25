# CS160

Up and running on MacOS
Install brew:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install ffmpeg
python3 execute.py <path_to_video>
# make sure absolute path to the root of the project contains no spaces or else...

If need more then one version of python running on the machine, use:
https://stackoverflow.com/questions/18671253/how-can-i-use-homebrew-to-install-both-python-2-and-3-on-mac


To run backend on local:
pip install -r requirements.txt
cd backend && python manage.py runserver

Then you can access the web page on local at http://127.0.0.1:8000/

# Andrey Lubenets

Back end:
To run the final version of back end, you have to issue following command:
python3 final_program.py
At this moment, the path to the file is indicated in this file, but it will be changed to be passed as a parameter soon.
You will have to install different packages such as dlib, ffmpeg, and others.
