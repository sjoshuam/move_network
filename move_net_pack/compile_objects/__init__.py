'''compile data from across different sources'''

##### IMPORT NEEDED CODED

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

# import built-in classes
import abc, pickle

# import additional packages
import pandas as pd

# get class objects for previous stages
from move_net_pack.get_data.m11_get_census_data import get_census_data
from move_net_pack.get_data.m12_get_move_data import GetIRSData
from move_net_pack.get_data.m13_get_geo_data import GetGeoData

from move_net_pack.refine_data.m21_refine_census_data import RefineCensusData
from move_net_pack.refine_data.m22_refine_move_data import RefineMoveData
from move_net_pack.refine_data.m23_refine_geo_data import RefineGeoData

##### DEFINE INHERITABLE ABSTRACT CLASS CLASSES

class CompileObjects(abc.ABC):

    def __init__(self, roster:list):

        # inventory datasets
        self.data_urls = dict()
        [self.data_urls.update(i.data) for i in roster]
        [setattr(self, i, self.data_urls[i]) for i in self.data_urls]

        # set status
        self.status = {
            'assemble_data': False,
            'fix_missing':   False,
            'save_data':     False,
        }

        # create slots for attributes
        self.data = None

        # load dictionary for states
        self.state_dict = settings.data_dict['state_dict']
        self.state_dict = pd.DataFrame(
            data=self.state_dict['columns'],
            columns=self.state_dict['header']
        )

    @utilities.govern_print_verbosity
    def __str__(self):

        # assess pipeline
        pipeline = list()
        for i in self.status.keys():
            if self.status[i]:
                pipeline += [i]
        pipeline = '\n[PIPELINE STATUS] ' + ' -> '.join(pipeline)

        # report which dataset index is the gold standard
        gold_standard = '[GOLD STANDARD INDEX] ' + self.gold_standard_index

        # report columns in dataset
        columns = self.data.columns.to_list()

        # report rows by year and states
        row_count = ['year','id_state','id_county', 'y1_id_state','y1_id_county']
        row_count = [i for i in row_count if i in self.data.reset_index().columns]
        row_count = self.data.reset_index()[row_count].groupby('year').nunique()
        row_count = '[ROW COUNT]\n' + utilities.capture_output(row_count.T)

        # assess missing data
        na_count = self.data.isna().sum()
        if na_count.sum() > 0: na_count = na_count.loc[na_count > 0]
        else: na_count = '< No NA found >'
        if self.data is not None:
            na_count = '[NA COUNTS]\n' + utilities.capture_output(na_count)
        else: na_count = '< No data found >'

        ## assemble message
        msg = '\n'.join([pipeline, gold_standard, row_count, na_count])
        return msg

    def assemble_data(self, roster):

        # evaluate initial status
        self.gold_standard_index = roster[0]
        roster = {i:True for i in roster}
        roster = {i:i in self.data_urls.keys() for i in roster.keys()}
        assert all(roster.values()), 'ERROR: There are missing datasets' +\
            utilities.capture_output(roster)

        # Read in and compile data
        for i in roster.keys():
            with open(self.data_urls[i], 'rb') as conn:
                if self.data is None:
                    self.data = pickle.load(conn)
                    conn.close()
                else:
                    temp = pickle.load(conn)
                    self.data = self.data.merge(
                        right=temp,
                        how='left', left_index=True, right_index=True,
                        suffixes=(None, '_DROP')
                        )
                    keep_index = list()
                    [keep_index.append(j) for j in self.data.columns if not j.endswith('_DROP')]
                    self.data = self.data[keep_index]

        # evaluate final status
        self.status['assemble_data'] = True
        print(self)
        return self

    @abc.abstractmethod
    def fix_missing(self):
        return self

    @abc.abstractmethod
    def save_data(self):
        return self

    @abc.abstractmethod
    def execute(self):
        return self.assemble_data().fix_missing().save_data()


##### TEST CODE

if __name__ == '__main__':

    # get data urls for previous stages
    refine_objects = [
        RefineCensusData(previous_stage=get_census_data()),
        RefineMoveData(previous_stage=GetIRSData().execute()), 
        RefineGeoData(previous_stage=GetGeoData().execute())
        ]

    # instantiate class
    objects = CompileObjects(roster = refine_objects)
    print(objects)


##########==========##########==========##########==========##########==========