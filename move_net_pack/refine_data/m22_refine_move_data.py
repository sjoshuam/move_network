'''Remove data defects and derive columns needed for analysis -- irs data'''

##### IMPORT NEEDED CODED

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

## import predecessor function
from move_net_pack.get_data.m12_get_move_data import GetIRSData

# import abstract class for refining data
from move_net_pack.refine_data.__init__ import RefineData

# import built-in python packages
import pickle

# import add-on packages
import pandas as pd

##### DEFINE KEY CLASS

class RefineMoveData(RefineData):
    '''Load, remove defects and derive needed variables from migration data'''

    def __init__(self, previous_stage):
           super().__init__(previous_stage)
           self.data = {'move_data':'output/move_data.pkl'}

    @staticmethod
    def load_data_mapper(file_urls) -> pd.DataFrame:
        '''proceess each file'''
        dat_list = list()
        for i in file_urls:
            dat_list.append(pd.read_csv(i[1], dtype=str))
            j = len(dat_list) - 1
            dat_list[j]['year'] = i[0]
        return dat_list

    @staticmethod
    def load_data_reducer(file_list:list) -> pd.DataFrame:
        '''Combine all files'''

        # simplify list
        dat = list()
        for i in range(0, len(file_list)):
            for j in range(0, len(file_list[i])):
                dat.append(file_list[i].pop(0))

        ## compile datsets
        dat = pd.concat(dat, axis='rows').reset_index(drop=True)
        return dat

    def remove_defects(self):
        '''Remove data defects (types, missing, outliers, etc)'''

        # Evaluate initial status
        assert self.status['load_data'], 'ERROR: Execute load_data() first.'

        # drop extraneous columns and rename
        self.data = self.data[self.data_dict['columns']]
        self.data.columns = self.data_dict['name'].to_list()

        # do type conversion
        type_list = {self.data_dict.loc[i,'name']:self.data_dict.loc[i,'type'] for i in self.data_dict.index}
        self.data = self.data.astype(type_list)

        # decode missingness (turn -1 to NA)
        self.data[self.data == -1] = pd.NA

        # remove summation and catch-all codes
        i = (self.data['y1_fips_county'].astype(int) != 0)  & \
            (self.data['y2_fips_county'].astype(int) != 0)  & \
            (self.data['y1_fips_state'].astype(int)  <= 56) & \
            (self.data['y2_fips_state'].astype(int)  <= 56)
        self.data = self.data.loc[i]

        # calculate interpolation ratios
        temp = self.data.groupby('y1_fips_state').agg({
            'return_count':'sum', 'person_count':'sum', 'income_total':'sum'})
        temp['person/return'] = temp['person_count'] / temp['return_count']
        temp['income/person'] = temp['income_total'] / temp['person_count']
        temp = temp.drop(columns=['return_count','person_count','income_total'])
        temp = temp.reset_index()
        self.data = self.data.merge(right=temp, how='left', on='y1_fips_state')

        # interpolate suppressed cells (suppressed if < 10 returns)
        i = self.data['return_count'].isna()
        self.data.loc[i, 'return_count'] = 5
        self.data.loc[i, 'person_count'] = self.data.loc[i, 'return_count'] *\
            self.data.loc[i,'person/return']
        self.data.loc[i, 'income_total'] = self.data.loc[i, 'person_count'] *\
            self.data.loc[i,'income/person']

        # interpolate other misisng incomes
        i = self.data['income_total'].isna()
        self.data.loc[i, 'income_total'] = self.data.loc[i, 'person_count'] *\
            self.data.loc[i, 'income/person']
        
        # clean up interpolations
        self.data = self.data.round({'person_count':0, 'income_total':0})
        self.data = self.data.drop(columns=['person/return', 'income/person'])

        # Evaluate final status and return
        self.status['remove_defects'] = True
        print(self)
        return self

    def derive_data(self):
        '''Derive needed variables from ingredients -- ids, state usps codes,
        rates, percentages, units, etc...'''

        # confirm that remove_defects was executed
        assert self.status['remove_defects'], 'ERROR: Execute remove_defects() first.'

        # create node ids
        for i in ['y1_','y2_']:
            self.data.columns = [j.replace(i, '') for j in self.data.columns]
            self.data = self.data.merge(
                right = self.state_dict.drop(columns='name_state'),
                how = 'left', on='fips_state')
            self.data = self.data.rename(columns={'id_state':(i+'id_state')})
            self.data[i+'id_county'] = self.data[i+'id_state'] + self.data['fips_county']
            self.data = self.data.drop(columns=['fips_state', 'fips_county'])

        ## create edge id and set index
        self.data['id_edge'] = self.data['y1_id_county'] +'-'+ self.data['y2_id_county']
        self.data = self.data.set_index(['year', 'id_edge']).sort_index()

        # Evaluate final status and return
        self.status['derive_data'] = True
        print(self)

        # save data and store link
        data_url = 'output/move_data.pkl'
        with open(data_url, 'wb') as conn:
            pickle.dump(self.data, conn)
            conn.close
        self.data = {'move_data':data_url}

        return self

    def execute(self):
        '''Execute pipeline from end to end'''
        self.get_data_dict('soi_dict').load_data().remove_defects().derive_data()
        return self

##### TEST KEY CLASS
if __name__ == '__main__':
    previous_stage = GetIRSData().execute()
    irs_data = RefineMoveData(previous_stage=previous_stage)
    irs_data.execute()

##########==========##########==========##########==========##########==========
