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
import requests
import warnings, os, datetime

## load setting
param = dict()

##########==========##########==========##########==========##########==========##########==========
########## PULL COUNTY-TO-COUNTY MIGRATION DATA FROM IRS

class IrsData:

    def __init__(self):
        """Initialize a class instance"""
        self.data_from_file = dict()
        self.valid_years = list()
        self.move_data = pd.DataFrame()
        self.status = {
            'make_file_inventory': {
                'Method executed': 'No',
                'Latest retrieval': 'N/A', 'Website queried': 'No',
                'Available files': 'N/A', 'Date range': 'N/A',
                },
            'extract_move_data': {
                'Method executed': 'No', 'Total rows': 'N/A',
                'Total counties': 'N/A', 'Date range': 'N/A',
                }
            }
        return None

    def __str__(self):
        """display useful information on status of code"""

        ## access pipeline
        pipeline_status = list()
        for i in self.status.keys():
            pipeline_status.append(self.status[i]['Method executed'] == 'Yes')
        if all(set(pipeline_status)):
            pipeline_status = 'Complete'
        else:
            pipeline_status = 'INCOMPLETE'
        print(pipeline_status)
        #return pipeline_status


    
        ## compile status
        print_string = '==== Status of IRS data pipline ================' + '\n'
        print_string += 'Pipeline' + ': ' + pipeline_status + '\n'
        for i in self.status.keys():
            print_string += '\n' + i + '\n'
            for j in self.status[i].keys():
                print_string += '\t' + j +': '+ self.status[i][j] + '\n'


        return print_string
        
    
    def make_file_inventory(self, start_year=2011):
        """Download data files from irs, but not if they have already been downloaded"""

        ## create folders if they do not exist
        for iter in ['input', 'output']:
            if not os.path.isdir(iter):
                warnings.warn(f"Created new directory: {iter}")
                os.mkdir(iter)

        ## construct roster of files
        file_inventory: pd.DataFrame = pd.DataFrame({'year':range(start_year, pd.Timestamp.now().year-3)})
        file_inventory['status'] = 'unknown'
        file_inventory['file'] = file_inventory.apply(
            lambda row: f"input/countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
        file_inventory['url'] = file_inventory['file'].str.replace(
            pat="input/", repl="https://www.irs.gov/pub/irs-soi/")
        file_inventory['created'] = 'N/A'
        file_inventory= file_inventory.set_index('year')

        ## download files if they do not already exist
        for iter in file_inventory.index:
            if not os.path.isfile(path= file_inventory['file'].at[iter]):
                file_inventory['status'].at[iter] = 'Not found'
                file_inventory['created'].at[iter] = '1900-01-01'
                retrieved_data = requests.get(url= file_inventory['url'].at[iter])
                if retrieved_data.status_code == 200:
                    file_inventory['status'].at[iter] = 'Downloaded now'
                    file_inventory['created'].at[iter] = pd.Timestamp.now().strftime('%Y-%m-%d')
                    open(file_inventory['file'].at[iter], 'w').write(retrieved_data.text)
                else:
                    pass
            else: 
                file_inventory['status'].at[iter] = 'Downloaded before'
                i_creation_date = os.path.getctime(file_inventory['file'].at[iter])
                i_creation_date = pd.Timestamp(i_creation_date, unit='s').strftime('%Y-%m-%d')
                file_inventory['created'].at[iter] = i_creation_date

        ## store useful objects for future functions
        self.file_inventory = file_inventory
        self.valid_years = file_inventory.index[file_inventory['status'] != 'Not found']

        ## analyze outcomes from file retrieval
        mfi = 'make_file_inventory'
        assert not ('unknown' in set(file_inventory.status)), "Some file retrievals skipped"
        self.status[mfi]['Method executed'] = 'Yes'
        self.status[mfi]['Available files'] = str(len(self.valid_years))
        self.status[mfi]['Date range'] = str(min(self.valid_years)) +'-'+ str(max(self.valid_years))
        self.status[mfi]['Latest retrieval'] = file_inventory['created'].max()
        if not all(file_inventory['status'] == 'Downloaded before'):
            self.status[mfi]['Website queried'] = 'Yes'

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

        ## extract data from files (use memory conversation if needed)
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

        ## analyze outcomes for status logs
        emd = 'extract_move_data'
        self.status[emd]['Method executed'] = 'Yes'
        self.status[emd]['Total rows'] = str(self.move_data.shape[0])
        self.status[emd]['Total counties'] = str(len(set(
            self.move_data.index.get_level_values('origin'))))
        f = lambda x: str(x.min()) +'-'+ str(x.max())
        self.status[emd]['Date range'] = f(self.move_data.index.get_level_values('year'))


        return self

##########==========##########==========##########==========##########==========##########==========
########## PULL SHAPE FILES FROM CENSUS TIGER

##########==========##########==========##########==========##########==========##########==========
########## CONSTRUCT TOP-LEVEL SCRIPT EXECUTION FUNCTION

class AllData:

    def __init__(self):
        """Initialize a class instance"""
        pass

    def acquire_data(self, verbose=False):
        """Executes all data retrieval and extraction function"""

        ## retrieve county to county migration data from IRS
        irs_data = IrsData()
        irs_data.make_file_inventory()
        irs_data.extract_move_data()
        if verbose: print(irs_data)

        ## retrieve GIS data from Census (TIGER) TODO
        #tiger_data = TIGER()

        ## retrieve weather data from NOAA or Meteostat (county-level) TODO

        ## retrieve economic data from BEA (CBSA-level) TODO

        ## retrieve political data from Harvard's Dataverse (state-level) TODO


        ## return final product TODO
        return None
    
    def consolidate_data(self):
        """Consolidate data into node and edge files"""
        pass


########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':

    ## time execution
    start_time = pd.Timestamp.now()

    ## get all data needed to measure node relations (edges and GIS)
    all_data = AllData().acquire_data(verbose=True)


    ## print execution time
    print('Execution time:', pd.Timestamp.now() - start_time)
    

##########==========##########==========##########==========##########==========##########==========
