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
