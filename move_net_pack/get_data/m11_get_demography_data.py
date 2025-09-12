'''Get American Community Survey (ACS) county data from the US Census Bureau'''


##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m01_define_settings import Settings
settings = Settings()

## import general utilities
from move_net_pack.m02_define_utilities import Utilities
utilities = Utilities()

## import module specific utilities
from move_net_pack.get_data import GetData

##### IMPORT CODE DEPENDENCIES

## TODO: finish generic method in utilities

##### TEST THE CODE

if __name__ == '__main__':

    get_data = GetData(
        file_url='input/census_acs_population_{year}.json',
        api_url='https://api.census.gov/data/{year}/acs/acs5/subject',
        api_query='?get=NAME,S0101_C01_001E&for=county:*',
    )

    print(get_data)
    response = get_data.query_api()
    print(get_data)


##########==========##########==========##########==========##########==========
