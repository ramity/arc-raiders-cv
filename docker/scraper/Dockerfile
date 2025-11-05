FROM ubuntu:24.04

# Install dependencies
RUN apt update
RUN apt upgrade -y
RUN apt install -y git
RUN apt install -y ffmpeg
RUN apt install -y dotnet-sdk-8.0

# Build TwitchDownloader repo and add to path
RUN mkdir /usr/src/TwitchDownloader
RUN git clone https://github.com/lay295/TwitchDownloader.git /usr/src/TwitchDownloader
RUN cd /usr/src/TwitchDownloader && dotnet publish TwitchDownloaderCLI -p:PublishProfile=Linux
ENV PATH="/usr/src/TwitchDownloader/TwitchDownloaderCLI/bin/Release/net6.0/publish/Linux:${PATH}"

# Add "download" alias
RUN echo 'alias download="TwitchDownloaderCLI videodownload --quality 1080p60"' >> ~/.bashrc

WORKDIR /root/videos

ENTRYPOINT sleep infinity

# Example CLI invocation
# TwitchDownloaderCLI videodownload --id 2608011038 --output /root/videos/2608011038.mp4 --quality 1080p60 --beginning 0:50:08 --ending 01:20:18
# download --id 2608011038 --output /root/videos/2608011038.mp4 --beginning 0:50:08 --ending 01:20:18
