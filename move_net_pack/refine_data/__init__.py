'''Define an abstract class for retrieving data from internet sources'''

##### SET UP THE ENVIRONMENT

# import settings
from move_net_pack.m02_define_settings import Settings
settings = Settings()

# import utilities
from move_net_pack.m03_define_utilities import Utilities
utilities = Utilities()

# import built-in packages
import abc

#####  DEFINE ABSTRACT CLASS

class RefineData(abc.ABC):
    '''Define abstract class for refining data'''

    # initialize class
    def __init__(self, previous_stage):
        self.previous_stage = previous_stage
        self.roster = previous_stage.roster

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

##########==========##########==========##########==========##########==========
