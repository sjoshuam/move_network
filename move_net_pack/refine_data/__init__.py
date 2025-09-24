'''Define an abstract class for retrieving data from internet sources'''

##### SET UP THE ENVIRONMENT

# import settings & utilities
from move_net_pack.m02_define_settings import Settings
settings = Settings()
from move_net_pack.m03_define_utilities import Utilities
utilities = Utilities()

# import built-in packages
import abc

## import other packages
import pandas as pd

#####  DEFINE ABSTRACT CLASS

class RefineData(abc.ABC):
    '''Define abstract class for refining data'''

    # initialize class
    def __init__(self, previous_stage):
        self.previous_stage = previous_stage
        self.roster = previous_stage.roster
        self.data_dict = None

    def __str__():
        pass

    @abc.abstractmethod
    def load_data(self):
        '''Process data files'''
        return self

    @abc.abstractmethod
    def remove_defects(self):
        '''remove data defects (types, missing, outliers, etc)'''
        return self

    @abc.abstractmethod
    def derive_data(self):
        '''derive needed variables from ingredients -- ids, state usps codes,
        rates, percentages, units, etc...'''
        return self
    
    def interpolate_from_ratio(self, pop:str, var:str)-> pd.DataFrame:
        '''Interpolate missing from median population ratio'''
        temp = 'temp_int_workspace'
        self.data[temp] = self.data[var] / self.data[pop]
        self.data[temp] = self.data[pop] * self.data[temp].median()
        i = self.data[var].isna()
        self.data.loc[i, var] = self.data.loc[i, temp]
        self.data = self.data.drop(columns=temp)
        return self
    
    def get_data_dictionary(self, data_dict:str, settings=settings):
        '''Unpack data dictionary and attach to class instance'''

        # unpack dictionary for dataset
        self.data_dict = settings.data_dict[data_dict]
        self.data_dict = pd.DataFrame(
            data=self.data_dict['columns'],
            columns=self.data_dict['header']
        )

        # unpack dictionary for states
        self.state_dict = settings.data_dict['state_dict']
        self.state_dict = pd.DataFrame(
            data=self.state_dict['columns'],
            columns=self.state_dict['header']
        )

        return self





##########==========##########==========##########==========##########==========
