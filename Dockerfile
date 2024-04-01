FROM ubuntu:20.04

ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /vms_object_detection_server

COPY . .

RUN apt-get update && \
    apt-get install -y ffmpeg tmux python3 python3-pip libglib2.0-0 libgl1-mesa-glx vim git

RUN ln -s $(which python3) /usr/bin/python

RUN pip install jupyter pandas fastapi[all] python-multipart jupyter fastapi_utils loguru pytest requests

