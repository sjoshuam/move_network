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
        self.roster = previous_stage.roster
        del previous_stage
        self.data_dict = None
        self.data = None
        self.status = {
            i:False for i in ['load_data', 'remove_defects', 'derive_data']}

    @utilities.govern_print_verbosity
    def __str__(self):

        ## set up basic template
        msg = ['\n','[PIPELINE]','-','[SUBSET]','-','[DISTRIBUTION]','-',
            '[SHAPE]','-','[NA COUNT]','-','\n']

        ## capture information
        try:
            # simply pipeline status
            msg[2] = list()
            for i in self.status.keys():
                if self.status[i]: msg[2] += [i]
            msg[2] = ' -> '.join(msg[2])

            # capture basic shape
            msg[8] = str(self.data.shape)

            # capture data subset
            index = self.data.shape[0] // 9
            index = range(index, self.data.shape[0], index)
            msg[4] = utilities.capture_output(self.data.iloc[index].T)

            # capture ranges
            f = [0, .25, .5, .75, 1]
            f = {i:lambda x,q=i: x.quantile(q) for i in f}
            msg[6] = self.data.select_dtypes(include='number').apply(f.values())
            msg[6].index = f.keys()
            msg[6] = utilities.capture_output(msg[6].T.round(1))

            # count NA values by column
            msg[10] = utilities.capture_output(self.data.isna().sum())

        except Exception as xcept:
            pass
        return '\n'.join(msg)
        

    def load_data(self):
        '''Read in census file and process'''

        # Evaluate initial status
        file_urls = [(i, self.roster[i]['file']) for i in self.roster.keys()]

        # iterate through raw data files
        self.data = utilities.run_in_parallel(
            iterable=file_urls,
            mapper=self.load_data_mapper,
            reducer=self.load_data_reducer,
            )
        self.data = self.data.reset_index()
        
        ## Evaluate final status
        self.status['load_data'] = True
        print(self)

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
    
    @staticmethod
    def assess__defects(dat: pd.DataFrame) -> str:
        'Assess how many cells having missing or outlier data'
        test = dat.apply(pd.to_numeric, errors = 'coerce').apply(
            lambda x: ((x-x.mean())/x.std()).abs()>=3)
        test = (test.isna().sum().sum(), test.sum().sum())
        test = '{} missing/{} outliers'.format(*test)
        return test
    
    def get_data_dict(self, data_dict:str, settings=settings):
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

    def execute(self):
        '''Run entire class pipeline'''
        self.load_data().remove_defects().derive_data()
        return self

##########==========##########==========##########==========##########==========
