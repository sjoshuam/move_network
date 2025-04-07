#!/bin/bash

## TIMEZONE: set the timezone
timedatectl set-timezone America/New_York

## UPGRADE: apply all updates for a non-mac unix system
if [ ! $(uname) = "Darwin" ]; then
  apt-get update
  apt-get dist-upgrade -y
  apt-get autoremove -y
  apt-get autoclean -y
fi


## SSH SERVER: set up ssh server for a non-mac unix system
if [ ! $(uname) = "Darwin" ]; then
  apt-get install openssh-server -y
  systemctl start ssh
  systemctl enable ssh
  echo "SSH login:" $(whoami)"@"$(hostname -I)
  ## systemctl stop ssh
fi

    #### notes
    ## mac: system preferences > sharing > remote login
    ## Check server status: systemctl status ssh
    ## Shut down server: systemctl stop ssh


# SSH KEYS: set up ssh keys
if [ -d "~/.ssh" ]; then mkdir ~/.ssh; fi
ssh-keygen -t ed25519 -C $(hostname) -f ~/.ssh/id_ed25519
echo "== ADD THIS KEY TO GITHUB ========"
cat ~/.ssh/ed25519.pub

    #### notes
    ## ssh-keygen -t rsa -b 4096 -C $(hostname) -f ~/.ssh/ed25519


## BASHRC:  modify the bashrc file
if [ ! -f "~.bashrc_backup" ]; then cp ~/.bashrc ~/.bashrc_backup; fi
cp ~/.bashrc_backup ~/.bashrc


## UTILITIES: install various useful software
apt-get install ca-certificates curl -y # web untilities

    #### notes
    ## basic loop: for iter in a b c; do echo iter; done


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
