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
import pandas as pd
from warnings import warn
from typing import Union
import requests, os


## load setting
param = dict()

########## BUILD TOP-LEVEL FUNCTION AND CLASS INTEGRATION

## define data classes

class MoveData:
    '''TODO'''

    def __init__(self):
        pass




## define top-level function




########## PULL COUNTY-TO-COUNTY MIGRATION DATA FROM IRS

def get_irs_movement_data():
    """Download csv files from irs"""

    ## create folders if they do not exist
    for iter in ['input', 'output']:
        if not os.path.isdir(iter):
            warn(f"Created new directory: {iter}")
            os.mkdir(iter)

    ## construct roster of files
    file_roster: pd.DataFrame = pd.DataFrame({'year':range(2011, pd.Timestamp.now().year)})
    file_roster['status'] = 'unknown'
    file_roster['file'] = file_roster.apply(
        lambda row: f"countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
    file_roster['url'] = file_roster.apply(
        lambda row: f"https://www.irs.gov/pub/irs-soi/{row['file']}", axis= 1)
    file_roster= file_roster.set_index('year')

    ## download files if they do not already exist
    for iter in file_roster.index:
        if not os.path.isfile(path= 'input/'+file_roster['file'].at[iter]):
            file_roster['status'].at[iter] = 'Not found'
            retrieved_data = requests.get(url= file_roster['url'].at[iter])
            if retrieved_data.status_code == 200:
                file_roster['status'].at[iter] = 'Downloaded now'
                open('input/'+file_roster['file'].at[iter], 'w').write(retrieved_data.text)
        else: 
            file_roster['status'].at[iter] = 'Downloaded before'

    ## communicate outcomes from file retrieval
    assert not ('unknown' in set(file_roster.status)), "Some file retrievals skipped"
    print('==== File retrieval outcomes ================')
    print(file_roster['status'].value_counts().sort_index())

    ## define function to read each file and extract
    def process_move_data(file: str) -> pd.DataFrame:
        """Extract useful information from a csv file"""
        cols= {'y1_statefips':str, 'y1_countyfips':str, 'y2_statefips':str}
        cols.update({'y2_countyfips':str, 'n2':int, 'agi':int})
        move_data= pd.read_csv(file, usecols= cols.keys(), dtype= cols)
        move_data= move_data.loc[move_data['y1_statefips'].astype(int)< 57]
        move_data= move_data.rename(
            {'n2':'people', 'y2_statefips':'dest', 'y1_statefips':'origin'}, axis= 1)
        move_data['dest']= move_data['dest'] + move_data['y2_countyfips']
        move_data['origin']= move_data['origin'] + move_data['y1_countyfips']
        move_data = move_data.drop(['y1_countyfips', 'y2_countyfips'], axis= 1)
        return move_data
    

    move_data= process_move_data('input/'+file_roster['file'].at[2011])
    print(move_data)

    ## execute data extraction function in parallel on all files

    ## construct MoveData class object


########## PULL COUNTY CHARACTERISTICS DATA FROM BEA (OR CENSUS IF THAT'S BETTER)


########## MAKE CODE AUTOMATICALLY QUERY FOR FUTURE YEARS


########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## create a spark session
    x = get_irs_movement_data()

    ## pull in county to county migration data from IRS
    pass


##########==========##########==========##########==========##########==========##########==========
