#!/bin/bash

port_num="1"
CONTAINER_NAME="geon_redis"
IMAGE_NAME="hub.inbic.duckdns.org/ai-dev/python_object_detection_server"
TAG="0.1"

port_num="1"
fastapi_RESTAPI_server_path=$(pwd)


docker run \
    --runtime nvidia \
    --gpus all \
    -it \
    -p ${port_num}1000:9000 \
    -p ${port_num}4379:6379 \
    -p ${port_num}4444:8888 \
    --name ${CONTAINER_NAME} \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${fastapi_RESTAPI_server_path}:/fastapi_RESTAPI_server \
    -e DISPLAY=$DISPLAY \
    --restart=always \
    -w /fastapi_RESTAPI_server  \
    ${IMAGE_NAME}:${TAG}
