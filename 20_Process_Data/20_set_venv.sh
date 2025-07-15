#!/bin/bash

python3 -m venv .venv_20
source .venv_20/bin/activate
pip install --upgrade pip --quite --no-input
pip install pandas pyspark requests geopandas shapely  --quiet --no-input
pip freeze > .venv_20/requirements.txt

if [ ! -d "20_Process_Data" ]
  then echo "Making dir" && mkdir 20_Process_Data
fi

if [ ! -d "20_Process_Data/Input" ]
  then echo "Making dir" && mkdir 20_Process_Data/Input && mkdir 20_Process_Data/Output
fi


## reason for each package
## pandas, pyspark - basic data manipulation
## requests - api interactions
## geopandas & shapely - GIS data manipulation
