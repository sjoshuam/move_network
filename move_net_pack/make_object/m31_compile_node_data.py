'''Compile all node (county data)'''

##### IMPORT CODE

# built-in packages
import pickle

# additional packages
import pandas as pd

# class objects for previous stages
from move_net_pack.get_data.m11_get_census_data import get_census_data
from move_net_pack.get_data.m12_get_move_data import GetIRSData
from move_net_pack.get_data.m13_get_geo_data import GetGeoData

from move_net_pack.refine_data.m21_refine_census_data import RefineCensusData
from move_net_pack.refine_data.m22_refine_move_data import RefineMoveData
from move_net_pack.refine_data.m23_refine_geo_data import RefineGeoData

##### DEFINE CORE CLASS

class NodeData:

    def __init__(self, refine_objects:list):
        self.data_urls = dict()
        [self.data_urls.update(i.data) for i in refine_objects]

    # TODO: ADD THE REST

    def execute(self):
        print(self.data_urls)
        return self



##### TEST CODE

if __name__ == '__main__':

    # get data urls for previous stages
    refine_objects = [
        RefineCensusData(previous_stage=get_census_data()),
        RefineMoveData(previous_stage=GetIRSData().execute()), 
        RefineGeoData(previous_stage=GetGeoData().execute())
        ]

    # instantiate class
    node_data = NodeData(
        refine_objects = refine_objects
        )
    node_data.execute()

##########==========##########==========##########==========##########==========
