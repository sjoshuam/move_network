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
import warnings, requests, os, multiprocessing


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

def download_irs_data():
    """Download csv files from irs, but not if they have already been downloaded"""

    ## create folders if they do not exist
    for iter in ['input', 'output']:
        if not os.path.isdir(iter):
            warnings.warn(f"Created new directory: {iter}")
            os.mkdir(iter)

    ## construct roster of files
    data_inventory: pd.DataFrame = pd.DataFrame({'year':range(2011, pd.Timestamp.now().year)})
    data_inventory['status'] = 'unknown'
    data_inventory['file'] = data_inventory.apply(
        lambda row: f"countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
    data_inventory['url'] = data_inventory.apply(
        lambda row: f"https://www.irs.gov/pub/irs-soi/{row['file']}", axis= 1)
    data_inventory= data_inventory.set_index('year')

    ## download files if they do not already exist
    for iter in data_inventory.index:
        if not os.path.isfile(path= 'input/'+data_inventory['file'].at[iter]):
            data_inventory['status'].at[iter] = 'Not found'
            retrieved_data = requests.get(url= data_inventory['url'].at[iter])
            if retrieved_data.status_code == 200:
                data_inventory['status'].at[iter] = 'Downloaded now'
                open('input/'+data_inventory['file'].at[iter], 'w').write(retrieved_data.text)
        else: 
            data_inventory['status'].at[iter] = 'Downloaded before'

    ## communicate outcomes from file retrieval
    assert not ('unknown' in set(data_inventory.status)), "Some file retrievals skipped"
    print('==== File retrieval outcomes ================')
    print(data_inventory['status'].value_counts().sort_index())
    return data_inventory


########## REFINE IRS DATA

def process_irs_data(file: str) -> pd.DataFrame:
    """Extract useful information from a csv file"""

    ## read in useful columns
    cols= {'y1_statefips':str, 'y1_countyfips':str, 'y2_statefips':str}
    cols.update({'y2_countyfips':str, 'n2':int, 'agi':int})
    move_data= pd.read_csv(file, usecols= cols.keys(), dtype= cols)

    ## filter out summary codes and improve column name interpretability
    move_data= move_data.loc[move_data['y1_statefips'].astype(int)< 57]
    move_data= move_data.rename(
        {'n2':'people', 'y2_statefips':'dest', 'y1_statefips':'origin'}, axis= 1)
    
    ## assemble full fips codes
    move_data['dest']= move_data['dest'] + move_data['y2_countyfips']
    move_data['origin']= move_data['origin'] + move_data['y1_countyfips']
    move_data = move_data.drop(['y1_countyfips', 'y2_countyfips'], axis= 1)
    return move_data

    #move_data= process_move_data('input/'+file_roster['file'].at[2011])
    #print(move_data)


########## DEFINE CLASS FOR IRS DATA (OR LEAVE AS A DATAFRAME?)


########## PULL COUNTY CHARACTERISTICS DATA FROM BEA (OR CENSUS IF THAT'S BETTER)



########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## initate a parallel processing pool
    pool= multiprocessing.Pool(processes= min(max(os.cpu_count() // 2, 1), 8))

    ## download irs data (if not already downloaded)
    irs_data_inventory= download_irs_data()

    ## process and compile data
    #irs_data= pool.map_async(
    #    func= process_irs_data,
    #    callback= lambda x:x, TODO: construct class
    #    iterable= [1, 2, 3]#irs_data_inventory TODO:  extract a simple iterable
    #)


##########==========##########==========##########==========##########==========##########==========
