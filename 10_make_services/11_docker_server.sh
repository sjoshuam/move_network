#!/bin/bash

echo -e "\nWARNING: This script has been tested piece by piece,
but not all the way through. Execute with caution.\n"


## DOCKER: install docker
curl -fsSL https://get.docker.com -o install-docker.sh
sh install-docker.sh && rm install-docker.sh
apt-get install -y uidmap
dockerd-rootless-setuptool.sh install


  ## add variables to bashrc
echo -e "\n# Docker Variables" >> ~/.bashrc
echo "export PATH=/usr/bin:$PATH" >> ~/.bashrc
echo "export DOCKER_HOST=unix:///run/user/$(id -u).docker.sock" >> ~/.bashrc


  ## start the server in rootless mode
systemctl --user start docker
systemctl --user enable docker


  ## download useful images
docker pull ubuntu:24.04 ## operating system
docker pull python:3.13 ## programming language
docker pull pytorch/manylinux-cuda124:latest ## deep learning + gpu processing
docker pull postgres:17.4 ## standards compliant sql database
docker pull neo4j:2025.02 ## graph database
docker pull apache/spark-py:v3.4.0 ## distributed analytics
docker pull elasticsearch:8.17.4 ## search engine

    #### notes
    ## check status: systemctl --user status docker
    ## stop docker: systemctl --user stop docker
    ## elasticsearch: docker pull elasticsearch:8.17 ## search engine

  