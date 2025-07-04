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

class IRS:

    #### initialize empty class instance
    def __init__(self):
        self.move_data = list()
        pass
    
    #### downloaded data files
    def make_file_inventory(self):
        """Download csv files from irs, but not if they have already been downloaded"""

        ## create folders if they do not exist
        for iter in ['input', 'output']:
            if not os.path.isdir(iter):
                warnings.warn(f"Created new directory: {iter}")
                os.mkdir(iter)

        ## construct roster of files
        file_inventory: pd.DataFrame = pd.DataFrame({'year':range(2011, pd.Timestamp.now().year)})
        file_inventory['status'] = 'unknown'
        file_inventory['file'] = file_inventory.apply(
            lambda row: f"input/countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
        file_inventory['url'] = file_inventory.apply(
            lambda row: f"https://www.irs.gov/pub/irs-soi/{row['file']}", axis= 1)
        file_inventory= file_inventory.set_index('year')

        ## download files if they do not already exist
        for iter in file_inventory.index:
            if not os.path.isfile(path= file_inventory['file'].at[iter]):
                file_inventory['status'].at[iter] = 'Not found'
                retrieved_data = requests.get(url= file_inventory['url'].at[iter])
                if retrieved_data.status_code == 200:
                    file_inventory['status'].at[iter] = 'Downloaded now'
                    open(file_inventory['file'].at[iter], 'w').write(retrieved_data.text)
                else:
                    pass
            else: 
                file_inventory['status'].at[iter] = 'Downloaded before'

        ## communicate outcomes from file retrieval
        assert not ('unknown' in set(file_inventory.status)), "Some file retrievals skipped"
        print('==== File retrieval outcomes ================')
        print(file_inventory['status'].value_counts().sort_index())
        self.file_inventory = file_inventory
        return self
    
    #### extract data from a file
    def extract_move_data_from_file(self, year) -> pd.DataFrame:
        """Extract useful information from a csv file"""

        ## read in useful columns
        cols= {'y1_statefips':str, 'y1_countyfips':str, 'y2_statefips':str}
        cols.update({'y2_countyfips':str, 'n2':int, 'agi':int})
        move_data= pd.read_csv(
            self.file_inventory.at[year, 'file'],
            usecols= cols.keys(), dtype= cols)

        ## filter out summary codes and improve column name interpretability
        move_data= move_data.loc[move_data['y1_statefips'].astype(int)< 57]
        move_data= move_data.rename(
            {'n2':'people', 'y2_statefips':'dest', 'y1_statefips':'origin'}, axis= 1)
    
        ## assemble full fips codes
        move_data['dest']= move_data['dest'] + move_data['y2_countyfips']
        move_data['origin']= move_data['origin'] + move_data['y1_countyfips']
        move_data = move_data.drop(['y1_countyfips', 'y2_countyfips'], axis= 1)
        self.move_data = move_data
        return self



########## REFINE IRS DATA



########## DEFINE CLASS FOR IRS DATA (OR LEAVE AS A DATAFRAME?)


########## PULL COUNTY CHARACTERISTICS DATA FROM BEA (OR CENSUS IF THAT'S BETTER)



########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## initate a parallel processing pool
    pool= multiprocessing.Pool(processes= min(max(os.cpu_count() // 2, 1), 8))

    ## download irs data (if not already downloaded)
    irs_data = IRS().make_file_inventory()
    irs_data.extract_move_data_from_file(2011)
    print(dir(irs_data))

    ## process and compile data
    #irs_data= pool.map_async(
    #    func= process_irs_data,
    #    callback= lambda x:x.head(5), #TODO: construct class
    #    iterable= 
    #)
    #print(irs_data)


##########==========##########==========##########==========##########==========##########==========
