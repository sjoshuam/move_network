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
           self.status = {
               'load_data': False,
               'remove_defects': False,
               'derive_data': False,
           }

    def __str__(self):
        msg = ['\n== RefineCensusData Status ========']
        for i in self.status.keys():
            msg += ['  '+i+': '+('EXECUTED' if self.status[i] else 'not executed')]
        return '\n'.join(msg) + '\n'

    @staticmethod
    def load_data_mapper(file_info):
        '''Mapper function for load_data'''
        data = list()
        for i in file_info:
            with open(i[1], 'rt') as conn:
                file_iter = '\n'.join(conn.readlines())
                conn.close()
            file_iter = json.loads(file_iter)
            file_iter = pd.DataFrame(
                data=file_iter[1::],
                columns=file_iter[0]
                )
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
        self.status['load_data'] = True
        return self

    def remove_defects(self):
        '''remove data defects -- types, missing, outliers, etc.'''

        # confirm that load_data was executed
        assert self.status['load_data'], 'ERROR: Execute load_data() first.'

        # give all variables human-interpretable names
        x = {'column':'year','name':'year','unit':'years','aggregate':'id','type':int}
        self.data_dict = pd.concat([pd.DataFrame([x]), self.data_dict])
        self.data = self.data.reset_index()
        self.data_dict['order'] = pd.Categorical(
            self.data_dict['column'], categories=self.data.columns)
        self.data_dict = self.data_dict.sort_values('order')
        self.data.columns = self.data_dict['name']

        ## Drop territories with too much missing data
        self.data['Defects'] = self.data.isna().sum(axis = 1)
        viable_state = self.data.groupby('fips_state').agg({'Defects':'mean'})
        viable_state = viable_state.loc[viable_state['Defects'] < 1].index
        self.data = self.data[self.data['fips_state'].isin(viable_state)]
        self.data = self.data.drop(columns='Defects')

        # year - convert to int
        self.data['year'] = self.data['year'].astype(int)

        # fips codes - str with fixed lengths
        self.data = self.data.astype({'fips_state':str, 'fips_county':str})
        self.data['fips_state'] = self.data['fips_state'].str.zfill(2)
        self.data['fips_county'] = self.data['fips_county'].str.zfill(3)

        # population -  positive int; will use as needed to interpolate other
        var = 'pop_age_all'; self.data = self.data.astype({var:int})
        
        # commute times - positive float
        var = 'commute_time'; self.data = self.data.astype({var:float})
        self.data[var] = self.data[var].clip(upper=60).mask(self.data[var]<0)
        self.data[var] = self.data[var].fillna(self.data[var].median())

        # unemployment variables - positive floats
        var = 'pop_unemp_all'
        self.data[var] = self.data[var].astype(float)
        self.interpolate_from_ratio(pop='pop_age_all', var=var)
        self.data[var] = self.data[var].round().astype(int)


        var = 'pop_unemp_rate'; self.data = self.data.astype({var:float})
        i = self.data[var]<0
        self.data[var] = self.data[var].mask(i).fillna(self.data[var].median())
        self.data[var] /= 100

        # age variables - positive int
        for var in ['pop_age_00-04', 'pop_age_05-09', 'pop_age_10-14', 'pop_age_65-69', 'pop_age_70-74', 'pop_age_75-79']:
            self.data[var] = self.data[var].astype(float).round().astype(int)

        # household costs and income - floats
        var = 'hh_cost_inc'; self.data = self.data.astype({var:float})
        i = self.data[var]<0
        self.data[var] = self.data[var].mask(i).fillna(self.data[var].median())

        var = 'hh_cost_cost'; self.data = self.data.astype({var:float})
        i = self.data[var]<0
        self.data[var] = self.data[var].mask(i).fillna(self.data[var].median())

        #  education variables - positive integers
        var = 'pop_edu_all'
        self.data[var] = self.data[var].astype(float).round().astype(int)
        var = 'pop_edu_ba'
        self.data[var] = self.data[var].astype(float).round().astype(int)
        var = 'pop_edu_ma+'
        self.data[var] = self.data[var].astype(float).round().astype(int)

        return self

    def derive_data(self):
        '''derive needed variables from ingredients -- ids, state usps codes,
        rates, percentages, units, etc.'''

        # usps(fips_state) + fips_county -> id_county
        self.data = self.data.merge(
            right=self.state_dict[['fips_state', 'id_state']],
            how='left', on='fips_state')
        self.data['id_county'] = self.data['id_state']+self.data['fips_county']

        # pop_unemp_all * pop_unemp_rate -> pop_job_not
        #  del: pop_unemp_rate
        var = 'pop_job_not'
        self.data[var] = self.data['pop_unemp_all'] * self.data['pop_unemp_rate']
        self.data[var] = self.data[var].round().astype(int)
        self.data = self.data.drop(columns='pop_unemp_rate')

        # pop_unemp_all - pop_job_not -> pop_job_job
        #   del: pop_unemp_all
        var = 'pop_job_job'
        self.data[var] = self.data['pop_unemp_all'] - self.data['pop_job_not']
        self.data = self.data.drop(columns='pop_unemp_all')

        # pop_age_00-04 + pop_age_05-09 + pop_age_10-14 -> pop_age_kid
        var = 'pop_age_kid'; parts = ['pop_age_00-04', 'pop_age_05-09', 'pop_age_10-14']
        self.data[var] = self.data[parts].sum(axis=1)
        self.data = self.data.drop(columns=parts)

        # pop_age_00-04 + pop_age_05-09 + pop_age_10-14 -> pop_age_old
        var = 'pop_age_old'; parts = ['pop_age_65-69', 'pop_age_70-74', 'pop_age_75-79']
        self.data[var] = self.data[parts].sum(axis=1)
        self.data = self.data.drop(columns=parts)

        ## Create a three category age breakdown, fixes the pre-2017 rate issue
        i = self.data['year'] < 2017
        self.data['pop_age_etc'] = self.data['pop_age_all'].copy()
        for var in ['pop_age_kid', 'pop_age_old']:
            self.data.loc[i, var] *= (self.data.loc[i, 'pop_age_all'] / 100)
            self.data[var] = self.data[var].round().astype(int)
            self.data['pop_age_etc'] -= self.data[var]
        self.data = self.data.drop(columns='pop_age_all')


        # log(hh_cost_cost / hh_cost_inc) -> hh_cost_cost

        # log(hh_cost_inc / median(hh_cost_inc)) -> hh_cost_inc

        # pop_edu_all - pop_edu_ba - pop_edu_ma+ -> pop_edu_etc
        #  del: pop_edu_all

        ## restore alphabetic column sorting
        self.data = self.data[sorted(self.data.columns)]
        self.data = self.data.set_index(['year','id_county']).sort_index()

        print(self.data.dtypes)
        print(self.data.iloc[range(0+3500, 30000, 3500)].T)
        print(self.data.select_dtypes(include='number').agg(['min', 'median', 'max']).T.round(1))

        for i in range(0, 3):
            print('TODO: FIX THE RATE ISSUE FOR EDU!!')

        return self


##### TEST KEY CLASS
if __name__ == '__main__':
    previous_stage = get_census_data()
    census_data = RefineCensusData(previous_stage=previous_stage)
    census_data.get_data_dictionary('acs_dict').load_data()
    census_data = census_data.remove_defects().derive_data()



##########==========##########==========##########==========##########==========
