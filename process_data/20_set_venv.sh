#!/bin/bash

if [ ! -d "20_Process_Data" ]
  then echo "Making dir" && mkdir 20_Process_Data
fi

cd 20_Process_data

python3 -m venv .venv_20
source .venv_20/bin/activate
pip install --upgrade pip --quiet --no-input
pip install pandas pyspark requests geopandas shapely  --quiet --no-input
pip freeze > .venv_20/requirements.txt



if [ ! -d "20_Process_Data/Input" ]
  then echo "Making dir" && mkdir Input && mkdir Output
fi


## reason for each package
## pandas, pyspark - basic data manipulation
## requests - api interactions
## geopandas & shapely - GIS data manipulation
