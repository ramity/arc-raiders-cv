FROM ubuntu:24.04

# Install dependencies
RUN apt update
RUN apt upgrade -y

# Install pip (Python3 is included in ubuntu without pip)
RUN apt install -y python3-pip

# Install python packages
RUN pip install --break-system-packages easyocr
RUN pip install --break-system-packages uvicorn
RUN pip install --break-system-packages fastapi
RUN pip install --break-system-packages pillow
RUN pip install --break-system-packages python-multipart

# Add "python" alias
RUN echo 'alias python="python3"' >> ~/.bashrc

WORKDIR /usr/src/ocr

ENTRYPOINT sleep infinity
