'''Remove data defects & derive columns -- census shapefiles'''

##### IMPORT NEEDED CODED

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

## import predecessor function
from move_net_pack.get_data.m13_get_geography_data import get_geography_data

# import abstract class for refining data
from move_net_pack.refine_data.__init__ import RefineData

## import built-in code
import json, pickle

# import data processing code and session
import pandas as pd


##########==========##########==========##########==========##########==========