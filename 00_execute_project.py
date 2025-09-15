'''Execute the move_network project from end to end'''

##### IMPORT CODE
# import settings
from move_net_pack.m01_define_settings import Settings
settings = Settings()

## import general utilities
from move_net_pack.m02_define_utilities import Utilities
utilities = Utilities()

## import module specific utilities
from move_net_pack.get_data.m11_get_census_data import get_census_data
from move_net_pack.get_data.m12_get_move_data import GetIRSData
from move_net_pack.get_data.m13_get_geography_data import GetGeoData
from move_net_pack.get_data.m14_get_polity_data import GetPolityData

##### DEFINE TOP-LEVEL CLASS

class MoveNetwork:
    '''Execute the move_network project from end to end'''

    def __init__(self):

        ## Track execution for each stage
        stages = ['get_data', 'refine_data', 'make_object', 'describe_object']
        stages += ['model_object', 'see_result']
        stages = {i:False for i in stages}
        self.status = stages

    def __str__(self):

        message = ['\n\n'+('='*2)+' Execution Status by Stage '+('='*8)+'\n']
        for i in self.status.keys():
            msg = (i+':').ljust(max([len(j) for j in self.status.keys()])+2,' ')
            msg += ('EXECUTED' if self.status[i] else 'not executed')
            message.append(msg)
        message = '\n'.join(message)

        return message

    def get_data(self):
        '''Stage 1.0: Get Data'''
        census_data = get_census_data()
        irs_data = GetIRSData().adjust_irs_api_links().query_api()
        geo_data = GetGeoData().query_api()
        polity_data = GetPolityData().adjust_polity_roster().query_api()
        self.status['get_data'] = True
        return None

    def refine_data(self):
        '''Stage 2.0: Refine Data'''
        assert self.status['get_data'], 'ERROR: run get_data() first'

        self.status['refine_data'] = True
        return None

    def make_object(self):
        '''Stage 3.0: Make Object'''
        assert self.status['refine_data'], 'ERROR: run refine_data() first'

        self.status['make_object'] = True
        return None
    
    def describe_object(self):
        '''Stage 4.0: Describe Object'''
        assert self.status['make_object'], 'ERROR: run make_object() first'

        self.status['describe_object'] = True
        return None
    
    def model_object(self):
        '''Stage 5.0: Model Object'''
        assert self.status['describe_object'], 'ERROR: run describe_object() first'

        self.status['model_object'] = True
        return None
    
    def see_result(self):
        '''Stage 6.0: See Result'''
        assert self.status['model_object'], 'ERROR: run model_object() first'

        self.status['see_result'] = True
        return None


##### TEST CODE
if __name__ == '__main__':
    move_network = MoveNetwork()
    move_network.get_data()
    print(move_network)





##########==========##########==========##########==========##########==========
