FROM ubuntu:24.04

# Install dependencies
RUN apt update
RUN apt upgrade -y
RUN apt install -y ffmpeg
RUN apt install -y build-essential

# Install pip (Python3 is included in ubuntu without pip)
RUN apt install -y python3-pip

# Install openai-whisper package
RUN pip install --break-system-packages openai-whisper

# Add "python" alias
RUN echo 'alias python="python3"' >> ~/.bashrc
RUN echo 'alias transcribe="python /usr/src/whisper/transcribe.py"' >> ~/.bashrc

WORKDIR /usr/src/whisper

ENTRYPOINT sleep infinity
