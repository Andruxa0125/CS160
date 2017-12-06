# Inherit from Heroku's python stack
FROM python:3.6.3-stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.7' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN set -x \
    && add-apt-repository ppa:mc3man/trusty-media \
    && apt-get install -y --no-install-recommends \
        ffmpeg

RUN cd /root && \
    git clone https://github.com/opencv/opencv.git && \
    cd ~/opencv && \
    mkdir release && \
    cd release && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
    make && \
    make install

COPY . /root/facefinder68

RUN cd /root/facefinder68/backend/facefinder/core/eyeLike && \
    rm -r build/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make

RUN cd /root/facefinder68 && \
    pip3 install -r requirements.txt

RUN apt-get install xvfb -y
#&& apt-get install xserver-xorg-core xserver-xorg-input-all \
#xserver-xorg-video-fbdev libx11-6 x11-common \
#x11-utils x11-xkb-utils x11-xserver-utils -y

#RUN cd /root/facefinder68/backend && \
#    python manage.py makemigrations && \
#    python manage.py migrate

CMD cd /root/facefinder68/backend && gunicorn --pythonpath backend backend.wsgi