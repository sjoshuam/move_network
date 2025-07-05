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

    def __init__(self):
        """Initialize a class instance"""
        self.data_from_file = dict()
        self.valid_years = list()
        self.move_data = pd.DataFrame()
        pass
        
    
    def make_file_inventory(self, start_year=2011):
        """Download data files from irs, but not if they have already been downloaded"""

        ## create folders if they do not exist
        for iter in ['input', 'output']:
            if not os.path.isdir(iter):
                warnings.warn(f"Created new directory: {iter}")
                os.mkdir(iter)

        ## construct roster of files
        file_inventory: pd.DataFrame = pd.DataFrame({'year':range(start_year, pd.Timestamp.now().year)})
        file_inventory['status'] = 'unknown'
        file_inventory['file'] = file_inventory.apply(
            lambda row: f"input/countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
        file_inventory['url'] = file_inventory['file'].str.replace(
            pat="input/", repl="https://www.irs.gov/pub/irs-soi/")
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

        ## store useful objects for future functions
        self.file_inventory = file_inventory
        self.valid_years = file_inventory.index[file_inventory['status'] != 'Not found']
        return self
    

    def extract_data_from_file(self, year) -> pd.DataFrame:
        """Extract useful information from a csv file"""

        ## read in useful columns
        cols= {'y1_statefips':str, 'y1_countyfips':str, 'y2_statefips':str}
        cols.update({'y2_countyfips':str, 'n2':int, 'agi':int})
        data_from_file= pd.read_csv(
            self.file_inventory.at[year, 'file'],
            usecols= cols.keys(), dtype= cols)

        ## filter out summary codes and improve column name interpretability
        data_from_file= data_from_file.loc[data_from_file['y1_statefips'].astype(int)< 57]
        data_from_file= data_from_file.rename(
            {'n2':'people', 'y2_statefips':'dest', 'y1_statefips':'origin'}, axis= 1)
        
        ## ensure leading zeros are included in fips codes
        cols = {'dest':2, 'origin':2, 'y2_countyfips':3, 'y1_countyfips':3}
        for i in cols.keys():
            data_from_file[i] = data_from_file[i].str.zfill(cols[i])

        ## assemble full fips codes
        data_from_file['dest']= data_from_file['dest'] + data_from_file['y2_countyfips']
        data_from_file['origin']= data_from_file['origin'] + data_from_file['y1_countyfips']
        data_from_file = data_from_file.drop(['y1_countyfips', 'y2_countyfips'], axis= 1)

        ## index and store
        data_from_file['year'] = year
        data_from_file = data_from_file.set_index(['year', 'origin', 'dest']).sort_index()
        self.data_from_file[year] = data_from_file
        return self
    

    def extract_move_data(self, conserve_memory=False):
        """ extract useful data from all valid files"""
        if conserve_memory:
            first_iteration = True
            for i in self.valid_years:
                self.extract_data_from_file(i)
                if first_iteration:
                    self.move_data = self.data_from_file[i].iloc[0:0]
                    first_iteration = False
                self.move_data = pd.concat(
                    [self.move_data, self.data_from_file[i]], axis=0, join='outer')
                del self.data_from_file[i]
        else:
            for i in self.valid_years:
                self.extract_data_from_file(i)
            self.move_data = pd.concat(self.data_from_file, axis=0, join='outer')
        return self


########## PULL COUNTY COORDINATES, ADD DISTANCES TO IRS DATA OBJECT & COORDS TO CENSUS
## Perhaps rename as edge and node data?


########## PULL COUNTY CHARACTERISTICS DATA FROM BEA (OR CENSUS IF THAT'S BETTER)


########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## time execution
    start_time = pd.Timestamp.now()

    ## retrieve irs county to county movement data
    irs_data = IRS().make_file_inventory()
    irs_data.extract_move_data()
    print(irs_data.move_data)

    ## print execution time
    print('Execution time:', pd.Timestamp.now() - start_time)
    

##########==========##########==========##########==========##########==========##########==========
