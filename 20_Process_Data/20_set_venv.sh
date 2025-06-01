#!/bin/bash

python3 -m venv .venv_20
source .venv_20/bin/activate
pip install pyspark --quiet --no-input

if [ ! -d "20_Process_Data" ]
  then echo "Making dir" && mkdir 20_Process_Data
fi

if [ ! -d "20_Process_Data/Input" ]
  then echo "Making dir" && mkdir 20_Process_Data/Input && mkdir 20_Process_Data/Output
fi
