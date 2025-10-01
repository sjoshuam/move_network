#!/bin/bash

## NOTE:  This script envisions Ubuntu 24.04 running Python 3.12

## Abort if not using the designated operating system 
if [ ! $(grep ^VERSION_ID=  /etc/os-release) == 'VERSION_ID="24.04"' ]; then
  echo 'ERROR: Script designed to run on Ubuntu 24.04; aborting...'
  exit 1
fi

if [ ! $(grep ^NAME=  /etc/os-release) == 'NAME="Ubuntu"' ]; then
  echo 'ERROR: Script designed to run on Ubuntu 24.04; aborting...'
  exit 1
fi

# discourage interactivity so scripts runs all the way through
export DEBIAN_FRONTEND=noninteractive

# update operating system
sudo apt-get update -y #qq
sudo apt-get upgrade -y #qq
sudo apt-get autoremove -y #qq
sudo apt-get install openjdk-21-jdk -y #qq

# Update python; abort if 3.12 isn't linked to python3
sudo apt-get install python3.12 -y #qq
sudo apt-get install python3-pip -y #qq
sudo apt-get install python3-venv -y #qq

if ! python3 -V 2>&1 | grep -q "^Python 3\.12"; then
  echo "ERROR: Script designed to run with Python 3.12"
  exit 2
fi

# undo the interactivity damper after apt-get installations are done
unset DEBIAN_FRONTEND

# build and activate virtual environment
python3.12 -m venv env
source env/bin/activate

# install packages
pip install pip --upgrade --no-input #--quiet

if [ ! -e requirements.txt ]; then
    pip install pandas pyspark scikit-learn dash --no-input #--quiet
    pip igraph geopandas geopy --no-input #--quiet
    pip install torch torchvision torch-geometric --no-input #--quiet
    pip install --upgrade certify #--quiet
    pip freeze > requirements.txt
  else
    pip install -r requirements.txt  --no-input #--quiet
fi

# set up directory structure
for i in input output product; do
  if [ ! -e $i ]; then
    mkdir $i
  else
    echo ''
  fi
done

# NOTE #1: may need to use this version to get maximum modeling performance
# pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129 --no-input --quiet

