'''
  This script executes work item #21 on the move network Kanban board: 
https://github.com/users/sjoshuam/projects/3  .  The script acquires the data necessary for the
project.  A key goal is sustainability -- the script have smart logic for when the data needs to
be refreshed with future years.
'''

##########==========##########==========##########==========##########==========##########==========


########## LIBRARIES AND SETTINGS
## Note: environment created with python3 -m venv venv_20; source .venv_20/bin/activate

## load libraries (built-in)
import warnings, os, json

## load libraries (venv extras)
import pandas as pd
import geopandas as gpd
import requests


## load setting
param = dict()

##########==========##########==========##########==========##########==========##########==========
########## GENERIC HELPER FUNCTIONS

def print_pipeline(self, name):
    """display useful information on status of a class-based pipeline"""
    pipeline_status = list()
    for i in self.status.keys():
        pipeline_status.append(self.status[i]['Method executed'] == 'Yes')
    if all(set(pipeline_status)):
        pipeline_status = 'Complete'
    else:
        pipeline_status = 'INCOMPLETE'

    ## compile status
    print_string = f'\n==== Status of {name} pipline ================' + '\n'
    print_string += 'Pipeline' + ': ' + pipeline_status + '\n'
    for i in self.status.keys():
        print_string += '\n' + i + '\n'
        for j in self.status[i].keys():
            print_string += '\t' + j +': '+ self.status[i][j] + '\n'
    return print_string


def get_credentials(file_loc=".credentials.json") -> pd.DataFrame:
    if os.path.isfile(file_loc):
        with open(".credentials.json") as credentials_conn:
            credentials = json.load(credentials_conn)
            return credentials
    else:
        raise Exception("Could not find an API credential file at the specified location")


##########==========##########==========##########==========##########==========##########==========
########## PULL COUNTY-TO-COUNTY MIGRATION DATA FROM IRS



class IrsData:
    """Class executes an ETL pipeline, retrieving county-to-county movement data from IRS"""

    def __init__(self):
        """Initialize a class instance"""
        self.data_from_file = dict()
        self.valid_years = list()
        self.move_data = pd.DataFrame()
        self.counties = list()
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
        return print_pipeline(self, 'IRS data')

    def make_file_inventory(self, start_year=2011):
        """Download data files from irs, but not if they have already been downloaded"""

        ## create folders if they do not exist
        for iter in ['input', 'output']:
            if not os.path.isdir(iter):
                warnings.warn(f"Created new directory: {iter}")
                os.mkdir(iter)

        ## construct roster of files
        file_inventory: pd.DataFrame = pd.DataFrame(
            {'year':range(start_year, pd.Timestamp.now().year-3)})
        file_inventory['status'] = 'unknown'
        file_inventory['file'] = file_inventory.apply(
            lambda row: f"input/irs_countyinflow{row['year']-2000}{row['year']-1999}.csv", axis= 1)
        file_inventory['url'] = file_inventory['file'].str.replace(
            pat="input/irs_", repl="https://www.irs.gov/pub/irs-soi/")
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
        """Extract useful information from an IRS county-to-county movement data csv file"""

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

        ## determine the most recent year in which each county appears in the data
        geography = self.move_data.reset_index()[['year', 'origin']]
        geography = geography.sort_values(by=['year','origin'], ascending=[False, True])
        geography = geography.drop_duplicates(subset=['origin']).reset_index(drop=True)
        self.geography = geography

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
########## PULL CBSA data from the BEA API

class BeaData:


    def __init__(self, years:list[int], credentials:dict[str]):
        "Initialize function"
        self.file_loc = 'input/bea_data.json'
        self.years = years
        self.credentials = credentials
        self.status = {
            'get_bea_data':{
                'Method executed':'No',
                'Latest retrieval':'',
                'Website queried':'',
            },
            'extract_bea_data':{
                'Method executed':'No',
                'Total MSA':'', 'Date range':'',
            },
        }


    def __str__(self):
        return print_pipeline(self, 'BEA data')

    def get_bea_data(self):
        "Query the BEA API to get CBSA data for "

        ## define useful variables
        f_name = 'get_bea_data'

        ## assemble url
        file_loc = self.file_loc
        url = f"https://apps.bea.gov/api/data/?UserID={self.credentials['BEA']}"
        url += "&method=GetData&datasetname=Regional&GeoFIPS=MSA&ResultFormat=json"
        url += f"&TableName=MARPP&LineCode=3"
        url += f"&Year={','.join([str(i) for i in self.years])}"

        ## download data if it has already been downloaded
        if os.path.isfile(file_loc):
            self.status[f_name]['Website queried'] = 'No'
        else:
            bea_data = requests.get(url)
            self.status[f_name]['Website queried'] = 'Yes'
            if bea_data.status_code == 200:
                with open(file_loc, 'wt') as conn:
                    conn.write(bea_data.text)
            else:
                self.status['f_name']['Total lines in file'] = -1

        ## tabulate statistics
        if os.path.isfile(file_loc):
            creation_date = pd.Timestamp(os.path.getctime(file_loc), unit='s')
            self.status[f_name]['Latest retrieval'] = creation_date.strftime('%Y-%m-%d')
        self.status[f_name]['Method executed'] = 'Yes'


    def extract_bea_data(self):
        """Extract data from raw json file"""
        pass

##########==========##########==========##########==========##########==========##########==========
########## PULL SHAPE FILES FROM CENSUS TIGER

class TigerData:

    def __init__(self, counties: pd.DataFrame):
        """Initialize function"""
        self.counties = counties
        self.cbsa = None
        self.gis = None
        self.status = {
            'get_gis (State)':{
                'Method executed': 'No',
                'Latest retrieval': '', 'Website queried': '',
                'Total rows': '', 'Total states': '', 'Vintage': '',
            },
            'get_gis (County)':{
                'Method executed': 'No',
                'Latest retrieval': '', 'Website queried': '',
                'Total rows': '', 'Total states': '', 'Vintage': '',
            },
            'get_gis (CBSA)':{
                'Method executed': 'No',
                'Latest retrieval': '', 'Website queried': '',
                'Total rows': '', 'Total states': '', 'Vintage': '',
            },
            'extract_gis':{
                'Method executed': 'No',
                'Geographies': 'USA', 'Total rows': '', 'NA count': '',
            },
            'get_old_gis':{
                'Method executed': 'No',
            },
            'clean_gis':{
                'Method executed': 'No',
                'Geographies':'USA', 'Total rows': '', 'NA count': '',
                'GEOID lengths': '', 'Coordinate range': '',
            },
        }


    def __str__(self):
        return print_pipeline(self, 'GIS data')
    

    def get_gis(self, geo_type:str, year:str):
        "Retrieve shapefiles from Census"

        ## assemble variables
        year = year
        file_name = f'tl_{year}_us_{geo_type.lower()}'
        web_url= f'https://www2.census.gov/geo/tiger/TIGER{year}/{geo_type.upper()}/{file_name}.zip'
        local_url = f'input/{file_name}.zip'
        f_name = f'get_gis ({geo_type})'
        key_cols = ['GEOID', 'STATEFP']

        ## download file unless it has already been downloaded
        if os.path.isfile(local_url):
            self.status[f_name]['Website queried'] = 'No'
            self.status[f_name]['Latest retrieval'] = pd.Timestamp(
                os.path.getctime(local_url), unit='s').strftime('%Y-%m-%d')
        else:
            gis_data = requests.get(url=web_url, verify=False)
            open(local_url, 'wb').write(gis_data.content)
            self.status[f_name]['Website queried'] = 'Yes'
            self.status[f_name]['Latest retrieval'] = pd.Timestamp.now().strftime('%Y-%m-%d')

        ## analyze downloaded data and log it
        gis_data = gpd.read_file(filename='zip://'+local_url+'!'+file_name+'.shp', columns=key_cols)
        self.status[f_name]['Vintage'] = str(year)
        self.status[f_name]['Total rows'] = str(gis_data.shape[0])
        if 'STATEFP' in gis_data.columns:
            self.status[f_name]['Total states'] = str(len(set(gis_data['STATEFP'])))
        self.status[f_name]['Method executed'] = 'Yes'

        ## return class object
        return self
    

    def extract_gis(self, geo_type:str, year:str):
        "extract coordinate data from gis files"

        ## assemble variables
        year = year
        local_url = f'zip://input/tl_{year}_us_{geo_type.lower()}.zip'
        local_url = local_url+f'!tl_{year}_us_{geo_type.lower()}.shp'
        f_name = 'extract_gis'
        key_cols = ['STATEFP', 'STUSPS', 'GEOID', 'INTPTLON', 'INTPTLAT', 'ALAND', 'NAME']

        ## extract data from
        gis = gpd.read_file(local_url, columns=key_cols).drop(columns=['geometry'])
        gis['geo_type'] = geo_type
        if self.gis is None:
            self.gis = gis
        else:
            self.gis = pd.concat([self.gis, gis], axis=0, join='outer', ignore_index=True)

        ## log outcomes
        self.status[f_name]['Geographies'] = self.status[f_name]['Geographies'] +', '+ geo_type
        self.status[f_name]['Total rows'] = str(self.gis.shape[0])
        self.status[f_name]['NA count'] = str(self.gis.isna().sum().sum())
        self.status[f_name]['Method executed'] = 'Yes'

        ## return class object
        return self
        

    def get_old_gis():
        pass


    def clean_gis(self):

        ## fill in missing usps state codes for counties
        crosswalk = self.gis.loc[self.gis['geo_type'] == 'State', ['STATEFP', 'STUSPS']]
        self.gis = self.gis.drop(columns=['STUSPS'])
        self.gis = pd.merge(self.gis, crosswalk, on='STATEFP', how='left')

        ## fill in missing usps and fips state codes for CBSA; simplify names
        self.gis['CBSA_usps'] = self.gis['NAME'].str.replace(
            pat=r".+, ([A-Z][A-Z])[^ ]*$", repl=r"\1", regex=True)
        cbsa_index = self.gis['geo_type'] == 'CBSA'
        self.gis.loc[cbsa_index, 'STUSPS'] = self.gis.loc[cbsa_index, 'CBSA_usps']
        self.gis = self.gis.drop(columns='CBSA_usps')
        self.gis.loc[cbsa_index, 'NAME'] = self.gis.loc[cbsa_index, 'NAME'].str.replace(
            r'-.*', r'', regex=True).str.replace(r', .*', r'', regex=True)
        self.gis = self.gis.drop(columns=['STATEFP'])
        self.gis = pd.merge(self.gis, crosswalk, on='STUSPS', how='left')

        ## sort columns
        col_order = ['geo_type','STUSPS','GEOID','INTPTLON','INTPTLAT','NAME','ALAND','STATEFP']
        assert set(col_order) == set(self.gis.columns), 'Columns do not match expectations'
        self.gis = self.gis[col_order].copy()

        ## convert numbers to float and convert aland to square miles
        self.gis = self.gis.astype({'INTPTLON':float, 'INTPTLAT':float, 'ALAND': float})
        self.gis['ALAND'] = (self.gis['ALAND'] / 2589988.110336).round(2)

        ## log results
        cg = 'clean_gis'
        self.status[cg]['Method executed'] = 'Yes'
        self.status[cg]['Geographies'] += ', '+', '.join(list(set(self.gis['geo_type'])))
        self.status[cg]['Total rows'] += str(self.gis.shape[0])
        self.status[cg]['NA count'] += str(self.gis.isna().sum().sum())
        self.status[cg]['GEOID lengths'] += ', '.join(
            self.gis['GEOID'].str.len().unique().astype(str).tolist())
        
        temp = self.gis[['INTPTLON', 'INTPTLAT']].agg(['min', 'max']).round(1).astype(str)
        temp = ' '.join(temp.agg(lambda x: '('+','.join(x)+')').to_list())
        self.status[cg]['Coordinate range'] = temp
        
        ## return class object
        return self


##########==========##########==========##########==========##########==========##########==========
########## CONSTRUCT TOP-LEVEL SCRIPT EXECUTION FUNCTION

class AllData:
    """Class executes all data ETL code in this script and compiles the results"""

    def __init__(self):
        """Initialize a class instance"""
        pass

    def acquire_data(self, verbose=False):
        """Executes all data retrieval and extraction function"""

        ## load credentials
        credentials = get_credentials()

        ## retrieve county to county migration data from IRS
        irs_data = IrsData()
        irs_data.make_file_inventory()
        irs_data.extract_move_data()
        if verbose: print(irs_data)

        ## retrieve weather data from NOAA or Meteostat (county-level) TODO

        ## retrieve economic data from BEA (CBSA-level) TODO
        if True:
            bea_data = BeaData(years=irs_data.valid_years, credentials=credentials)
            bea_data.get_bea_data()
            bea_data.extract_bea_data()
            if verbose: print(bea_data)
        else:
            Warning('BEA section disabled')

        ## retrieve political data from Harvard's Dataverse (state-level) TODO

        ## retrieve GIS data from Census (TIGER) TODO
        if False:
            tiger_data = TigerData(counties=irs_data.geography)
            for i in ['State', 'County', 'CBSA']:
                tiger_data.get_gis(i, max(irs_data.valid_years))
                tiger_data.extract_gis(i, max(irs_data.valid_years))
            tiger_data.clean_gis()
            if verbose: print(tiger_data)
        else:
            print('WARNING: Census Tiger section disabled')

        ## return final product TODO
        return None
    
    def consolidate_data(self):
        """Consolidate data into node and edge files"""
        pass

##########==========##########==========##########==========##########==========##########==========
##########==========##########==========##########==========##########==========##########==========

########## TEST EXECUTION OF ALL CODE

if __name__ == '__main__':
    all_data = AllData().acquire_data(verbose=True)
    

##########==========##########==========##########==========##########==========##########==========
##########==========##########==========##########==========##########==========##########==========
