'''Compile all node (county data)'''

##### IMPORT CODE

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

# built-in packages

# additional packages
import pandas as pd

## import module specific utilities
from move_net_pack.compile_objects import CompileObjects

# get class objects for previous stages (for testing)
from move_net_pack.get_data.m11_get_census_data import get_census_data
from move_net_pack.get_data.m12_get_move_data import GetIRSData
from move_net_pack.get_data.m13_get_geo_data import GetGeoData

from move_net_pack.refine_data.m21_refine_census_data import RefineCensusData
from move_net_pack.refine_data.m22_refine_move_data import RefineMoveData
from move_net_pack.refine_data.m23_refine_geo_data import RefineGeoData

##### DEFINE CORE CLASS
## TODO:  align nodes with county edgelist

class CompileEdges(CompileObjects):
    
    def __init__(self, roster):
        super().__init__(roster)
    
    def fix_missing(self):

        # evaluate initial status
        assert self.status['assemble_data'], 'ERROR: Run .assemble_data()'

        # limit states to the allowed list
        allowed_states = self.state_dict.loc[self.state_dict['use'],'id_state']
        allowed_states = allowed_states.to_list()
        index = self.data['y1_id_state'].isin(allowed_states) &\
            self.data['y2_id_state'].isin(allowed_states)
        self.data = self.data[index]

        # TODO: Fill in reciprical distances

        # TODO: Create zero edges

        # evaluate final status
        self.status['fix_missing'] = True
        print('TODO: Finish compile_edges/fix_missing')
        print(self)
        return self # TODO
    
    def save_data(self):

        # evaluate initial status
        assert self.status['fix_missing'], 'ERROR: Run .fix_missing()'

        # evaluate final status
        self.status['save_data'] = True
        print('TODO: compile_edges/save_data')
        #print(self)
        return self # TODO

    def execute(self, roster=['move_data', 'county_distance']):
            return self.assemble_data(roster).fix_missing().save_data()





##### TEST CODE

if __name__ == '__main__':

    # get data urls for previous stages
    refined_objects = [
        RefineCensusData(previous_stage=get_census_data()),
        RefineMoveData(previous_stage=GetIRSData().execute()), 
        RefineGeoData(previous_stage=GetGeoData().execute())
        ]

    # execute pipeline
    nodes = CompileEdges(roster=refined_objects).execute()

##########==========##########==========##########==========##########==========
