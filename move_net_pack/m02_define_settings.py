'''Defines key settings for use across all project scripts'''

#### IMPORT CODE

# load built-in packages
import os

## load custom code
from move_net_pack.m01_define_data_dictionaries import *

##### DEFINE CLASS TO HOLD SETTINGS
class Settings:
    '''Defines key settings for use across all project scrips'''

    def __init__(
        self,
        state_dict=state_dict, acs_dict=acs_dict, soi_dict=soi_dict,
        tiger_dict=tiger_dict, mit_dict=mit_dict,
        years=range(2011, 2020), verbose=True, cpus=os.cpu_count(),
        query=True, reload=False
        ):

        ## define an attribute for each sub-package
        self.subpack = ['execute_project', 'get_data', 'refine_data']
        self.subpack += ['make_object', 'describe_object', 'model_object']
        self.subpack += ['see_result', 'data_dict']
        for i in self.subpack:
            setattr(self, i, dict())
        self.execute_project = dict(years=years, verbose=verbose, cpus=cpus)
        self.get_data = dict(query=query, reload=reload)
        self.data_dict = dict(
            acs_dict=acs_dict, soi_dict=soi_dict, tiger_dict=tiger_dict,
            mit_dict=mit_dict, state_dict=state_dict
            )

    def __str__(self):

        ## Discover and record all settings
        message = list()
        for i in self.subpack:
            message += [('\n' + ('='*2) + ' {} ' + ('=' * 8)).format(i)]
            for j in getattr(self,i).keys():
                message += [j + ': ' + str(getattr(self,i)[j])]
        
        ## Express log if verbose set to True
        if self.execute_project['verbose']: message = '\n'.join(message)
        else: message = ''

        return message

##### TEST CLASS INSTANTIATION
if __name__ == '__main__':
    settings = Settings()
    print(settings)


##########==========##########==========##########==========##########==========
