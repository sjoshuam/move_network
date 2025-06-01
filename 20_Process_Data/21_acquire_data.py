'''
  This script executes work item #21 on the move network Kanban board: 
https://github.com/users/sjoshuam/projects/3  .  The script acquires the data necessary for the
project.  A key goal is sustainability -- the script have smart logic for when the data needs to
be refreshed with future years.
'''

##########==========##########==========##########==========##########==========##########==========


########## LIBRARIES AND SETTINGS
## Note: environment created with python3 -m venv venv_20; source .venv_20/bin/activate

## load libraries
from pyspark.sql import SparkSession

## load setting
param = dict()

########## BUILD TOP-LEVEL FUNCTION AND CLASS INTEGRATION

## define data classes

class MoveData:
    '''TODO'''

    def __init__(self, inflow:dict(), outflow:dict()):
        self.year = set(list(inflow.keys()) + list(outflow.keys()))
        self.inflow = inflow
        self.outflow = outflow
        assert inflow.keys() == outflow.keys(), "inflow/outflow data years don't match"
        self.year = set(inflow.keys())




## define top-level function




########## PULL COUNTY-TO-COUNTY MIGRATION DATA FROM IRS


########## PULL COUNTY CHARACTERISTICS DATA FROM BEA (OR CENSUS IF THAT'S BETTER)


########## MAKE CODE AUTOMATICALLY QUERY FOR FUTURE YEARS


########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## create a spark session
    spark = SparkSession.builder.appName("acquire_data")
    move_data = MoveData(
        inflow = {2022:1, 2021:2},
        outflow = {2021:1, 2022:2}
        )

    ## pull in county to county migration data from IRS
    print(move_data.year)
    pass


##########==========##########==========##########==========##########==========##########==========
