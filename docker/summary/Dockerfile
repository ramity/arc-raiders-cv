FROM ubuntu:24.04

# Install dependencies
RUN apt update
RUN apt upgrade -y

# Install pip (Python3 is included in ubuntu without pip)
RUN apt install -y python3-pip  

# Install transformers packages
RUN pip install --break-system-packages transformers
RUN pip install --break-system-packages torch

# Add "python" alias
RUN echo 'alias python="python3"' >> ~/.bashrc
RUN echo 'alias summarize="python /usr/src/summary/summarize.py"' >> ~/.bashrc

WORKDIR /usr/src/summary

ENTRYPOINT sleep infinity
