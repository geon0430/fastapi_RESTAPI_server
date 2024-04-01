#!/bin/bash

port_num="1"
CONTAINER_NAME="geon_vms_object_detection_server"
IMAGE_NAME="hub.inbic.duckdns.org/dev-1-team/vms_object_detection_server"
TAG="0.1"

port_num="1"
fastapiUiUx_path=$(pwd)


docker run \
    --runtime nvidia \
    --gpus all \
    -it \
    -p ${port_num}7000:7000 \
    -p ${port_num}6000:6000 \
    -p ${port_num}9999:8888 \
    --name ${CONTAINER_NAME} \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${fastapiUiUx_path}:/vms_object_detection_server \
    -e DISPLAY=$DISPLAY \
    --restart=always \
    -w /vms_object_detection_server \
    ${IMAGE_NAME}:${TAG}
