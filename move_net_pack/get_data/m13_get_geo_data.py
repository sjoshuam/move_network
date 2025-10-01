'''Get GIS data for all us counties'''


##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m02_define_settings import Settings
settings = Settings()

## import general utilities
from move_net_pack.m03_define_utilities import Utilities
utilities = Utilities()

## import module specific utilities
from move_net_pack.get_data import GetData


##### DEFINE IRS DATA RETRIVAL CLASS

class GetGeoData(GetData):

    def __init__(self,**kwargs):

        super().__init__(
            file_url='input/census_tiger_geo_{year}.zip',
            api_url='https://www2.census.gov',
            api_query='/geo/tiger/TIGER{year}/COUNTY/tl_{year}_us_county.zip',
            print_name='tiger_geo'
            )

    def execute(self):
        '''Execute the pipeline from end to end'''
        return self.query_api()
        
##### TEST THE CODE
if __name__ == '__main__':

    ## retrive irs data
    geo_data = GetGeoData().query_api()

##########==========##########==========##########==========##########==========
