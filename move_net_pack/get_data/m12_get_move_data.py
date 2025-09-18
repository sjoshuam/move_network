'''Get data on residential moves between US counties from IRS SOI'''

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

class GetIRSData(GetData):

    def __init__(self,**kwargs):

        super().__init__(
            file_url='input/irs_soi_moves_{year}.csv',
            api_url='https://www.irs.gov',
            api_query='/pub/irs-soi/countyoutflow[y0y1].csv',
            print_name='soi_moves'
            )

    def adjust_irs_api_links(self):
        '''Add customization to irs api urls'''
        for i in self.roster.keys():
            fix = str(i-2000).zfill(2) + str(i-1999).zfill(2)
            self.roster[i]['url'] = self.roster[i]['url'].replace('[y0y1]', fix)
        return self


##### TEST THE CODE
if __name__ == '__main__':

    ## retrive irs data
    irs_data = GetIRSData().adjust_irs_api_links().query_api()

##########==========##########==========##########==========##########==========
