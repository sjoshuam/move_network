#!/bin/bash



# update operating system
if [ $(uname -s) == 'Linux' ]; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get update -yqq
  sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yqq
fi

# build and activate virtual environment
python3.12 -m venv env
source env/bin/activate

# install packages
pip install pip --upgrade --no-input --quiet

if [ ! -e requirements.txt ]; then
    pip install pandas pyspark igraph dash scikit-learn --no-input --quiet
    pip torch torchvision torch-geometric --no-input --quiet
  fi
    pip freeze > requirements.txt
  else
    pip install -r requirements.txt  --no-input --quiet
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

