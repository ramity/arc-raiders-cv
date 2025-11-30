FROM ubuntu:24.04

# Install dependencies
RUN apt update
RUN apt upgrade -y

# Install pip (Python3 is included in ubuntu without pip)
RUN apt install -y python3-pip  

# Helper tool for querying installed libs
RUN apt install -y pkg-config

# Install Tesseract
# RUN apt install -y tesseract-ocr
# RUN pip install --break-system-packages pytesseract

# Install pip packages
RUN pip install --break-system-packages numpy
RUN pip install --break-system-packages matplotlib
RUN pip install --break-system-packages requests
RUN pip install --break-system-packages tqdm

# OpenCV dependencies
RUN apt install -y cmake g++ wget unzip
RUN apt install -y ffmpeg libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libx264-dev

# Download OpenCV code
RUN mkdir /root/opencv
RUN wget -O /root/opencv/opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
RUN wget -O /root/opencv/opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
RUN unzip /root/opencv/opencv.zip -d /root/opencv/
RUN unzip /root/opencv/opencv_contrib.zip -d /root/opencv/
RUN mkdir /root/opencv/build

# Configure OpenCV
RUN cd /root/opencv/build && cmake -DWITH_FFMPEG=1 -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules ../opencv-4.x

# Build and install OpenCV
RUN cd /root/opencv/build && make -j$(nproc)
RUN cd /root/opencv/build && make install

# Add "python" alias
RUN echo 'alias python="python3"' >> ~/.bashrc

WORKDIR /usr/src/analysis

ENTRYPOINT sleep infinity
