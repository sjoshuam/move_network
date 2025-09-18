'''Get county voting patterns data for all us counties'''


##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m02_define_settings import Settings
settings = Settings()

## import general utilities
from move_net_pack.m03_define_utilities import Utilities
utilities = Utilities()

## import module specific utilities
from move_net_pack.get_data import GetData

###### DEFINE HARVARD DATAVERSE (MIT ELECTION LAB) DATA RETRIVAL CLASS

class GetPolityData(GetData):

    def __init__(self):

        super().__init__(
            file_url='input/mit_eleclab_presvote.csv',
            api_url='https://dataverse.harvard.edu',
            api_query='/api/access/datafile/11986802?format=original',
            print_name='eleclab_presvote'
            )
        
    def adjust_polity_roster(self):
        '''No year iteration needed; slim down roster accordingly'''
        self.roster = {2011:self.roster[2011]}
        return self


##### TEST THE CODE
if __name__ == '__main__':

    ## retrive irs data
    polity_data = GetPolityData().adjust_polity_roster().query_api()