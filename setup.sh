#!/bin/bash

## Abort if not using the designated operating system 
if [ ! $(grep ^VERSION_ID=  /etc/os-release) == 'VERSION_ID="24.04"' ]; then
  echo 'ERROR: Script designed to run on Ubuntu 24.04; aborting...'
  exit 1
fi

if [ ! $(grep ^NAME=  /etc/os-release) == 'NAME="Ubuntu"' ]; then
  echo 'ERROR: Script designed to run on Ubuntu 24.04; aborting...'
  exit 1
fi

# update operating system
if [ $(uname -s) == 'Linux' ]; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get update -y #qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y #qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get autoremove -y #qq
fi

# Update python; abort if 3.12 isn't linked to python3
sudo apt-get install python3.12
sudo apt-get install python3-pip
sudo apt-get install python3-venv

if ! python3 -V 2>&1 | grep -q "^Python 3\.12"; then
  echo "ERROR: Script designed to run with Python 3.12"
  exit 2
fi


# build and activate virtual environment
python3.12 -m venv env
source env/bin/activate

# install packages
pip install pip --upgrade --no-input #--quiet

if [ ! -e requirements.txt ]; then
    pip install pandas pyspark igraph dash scikit-learn --no-input #--quiet
    pip install torch torchvision torch-geometric --no-input #--quiet
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

