#!/bin/bash

IMAGE_NAME="hub.inbic.duckdns.org/dev-1-team/vms_object_detection_server"
TAG="0.1"

docker build --no-cache -t ${IMAGE_NAME}:${TAG} .
