'''Move data defects and derive columns needed for analysis'''

##### IMPORT NEEDED CODED

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

## import predecessor function
from move_net_pack.get_data.m11_get_census_data import get_census_data

# import abstract class for refining data
from move_net_pack.refine_data.__init__ import RefineData

## import built-in code
import json

# import data processing code and session
import pandas as pd

##### DEFINE KEY CLASS

class RefineCensusData(RefineData):
    '''Class object for refining census data'''

    def __init__(self, previous_stage):
           super().__init__(previous_stage)

    @staticmethod
    def load_data_mapper(file_info):
        '''Mapper function for load_data'''
        data = list()
        for i in file_info:
            with open(i[1], 'rt') as conn:
                file_iter = '\n'.join(conn.readlines())
                conn.close()
            file_iter = json.loads(file_iter)
            file_iter = pd.DataFrame(data=file_iter[1::], columns=file_iter[0])
            file_iter['year'] = int(i[0][1])
            file_iter = file_iter.set_index(['year','state', 'county'])
            file_iter = file_iter.sort_index()
            data.extend([file_iter])
        return data
    
    @staticmethod
    def load_data_reducer(nested_list):
        '''Reducer function for load_data'''
        data = {i:list() for i in settings.execute_project['years']}

        ## sort data frames by year
        for i in range(0,len(nested_list)):
            for j in range(0,len(nested_list[i])):
                file_iter = nested_list[i].pop()
                year_iter = max(file_iter.index.get_level_values('year'))
                data[year_iter].append(file_iter)

        ## consolidate data
        for i in data.keys():
            data[i] = pd.concat(data[i],axis='columns')
        data = pd.concat(data.values(),axis='rows').sort_index()
        return data

    def load_data(self):
        '''Read in census file and process'''
        file_urls = [(i, self.roster[i]['file']) for i in self.roster.keys()]
        self.data = utilities.run_in_parallel(
            iterable=file_urls,
            mapper=self.load_data_mapper,
            reducer=self.load_data_reducer,
            )
        return self

    def remove_defects(self):
        '''remove data defects -- types, missing, outliers, etc.'''

        ## cast variables to proper type
        print(self.data.head(2))
        print(self.data.dtypes)
        return self

    def derive_data(self):
        '''derive needed variables from ingredients -- ids, state usps codes,
        rates, percentages, units, etc.'''
        return self


##### TEST KEY CLASS
if __name__ == '__main__':
    previous_stage = get_census_data()
    census_data = RefineCensusData(previous_stage=previous_stage)
    census_data = census_data.load_data()
    census_data = census_data.remove_defects()
    #census_data = census_data.derive_data()



##########==========##########==========##########==========##########==========
