'''Get American Community Survey (ACS) county data from the US Census Bureau'''


##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m02_define_settings import Settings
settings = Settings()

## import general utilities
from move_net_pack.m03_define_utilities import Utilities
utilities = Utilities()

## import module specific utilities
from move_net_pack.get_data import GetData

##### DEFINE CENSUS DATA NEEDS
census_data_dict = {
    # Population count by age: total, 0-4, 5-9, 10-14, 65-69, 70-74, 75-79
    'age': ['S0101_C01_001E', 'S0101_C01_002E', 'S0101_C01_003E', 'S0101_C01_004E', 'S0101_C01_015E', 'S0101_C01_016E', 'S0101_C01_017E'],
    # Population count by degree: Total, Bachelors, Graduate
    'edu': ['S1501_C01_006E', 'S1501_C01_012E', 'S1501_C01_013E'],
    # Population count by employment: Total, Unemployment rate
    'job': ['S2301_C01_001E', 'S2301_C04_002E'],
    # Median income:  Income, Monthly costs
    'cost': ['S2503_C01_013E', 'S2503_C01_024E', 'S2503_C01_028E'],
    # Mean time:  Worker commute
    'commute': ['S0801_C01_046E'],
    }
census_data_dict = {
    i:','.join(census_data_dict[i]) for i in census_data_dict.keys()}


##### DEFINE CENSUS DATA RETRIVAL FUNCTION

def get_census_data(data_dict=census_data_dict) -> dict:
    '''Get all data from census'''

    ## interatively retrieve all data from  census
    yr = '{year}'
    raw_rosters = dict()
    for i in data_dict.keys():
        get_data = GetData(
            file_url=f'input/census_acs_{i}_{yr}.json',
            api_url='https://api.census.gov/data/{year}/acs/acs5/subject',
            api_query=f'?get={data_dict[i]}&for=county:*',
            print_name=f'acs_{i}'
        )
        get_data.query_api()
        raw_rosters[i] = get_data.roster

    ## compile and simplify roster information
    roster = dict()
    for i in raw_rosters.keys():
        for j in raw_rosters[i].keys():
            roster[(i,j)] = raw_rosters[i][j]
    get_data.roster = roster
    return get_data


##### TEST THE CODE
if __name__ == '__main__':
    census_data = get_census_data()

    ## confirm roster
    print('-'*10)
    #print(census_data)


##########==========##########==========##########==========##########==========
