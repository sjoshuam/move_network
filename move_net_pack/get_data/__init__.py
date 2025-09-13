'''Define an abstract class for retrieving data from internet sources'''

##### SET UP THE ENVIRONMENT

# import settings
from move_net_pack.m01_define_settings import Settings
settings = Settings()

# import built-in packages
import pathlib, requests, time

# import utilities
from move_net_pack.m02_define_utilities import Utilities
utilities = Utilities()

##### DEFINE AN ABSTRACT CLASS FOR RETRIEVING DATA FROM THE INTERNET

class GetData():
    '''Define an abstract class for retrieving data from the web'''

    def __init__(
        self, file_url, api_url, api_query, print_name, settings=settings):

        # assemble roster of desired data files
        years = settings.execute_project['years']
        file_roster = {i:file_url.format(year=i) for i in years}

        # assemble roster of source urls
        url_roster = api_url + api_query
        url_roster = {i:url_roster.format(year=i) for i in years}

        # determine what files need to be downloaded
        if settings.get_data['reload']:
            {i:pathlib.Path(file_roster[i]).unlink(missing_ok=True) for i in years}
        found_file = {i:pathlib.Path(file_roster[i]).exists() for i in years}

        # compile data as unified class instance attribute.
        self.roster = dict()
        for i in years:
            self.roster[i] = dict(
                file=file_roster[i],
                url=url_roster[i],
                found=found_file[i],
                acquired=False
                )

        self.queried = False
        self.print_name = print_name
            
    @utilities.govern_print_verbosity
    def __str__(self):

        # tabulate outcomes
        found, acquired, missing = 0, 0, 0
        for j in self.roster.keys():
            i = self.roster[j]
            if i['found']: found += 1
            else:
                if i['acquired']: acquired += 1
                else: missing += 1

        # Formulate output
        message = f'GetData ({self.print_name}): '
        message += f'Of {len(self.roster)} files, {found} found, '
        message += f'{acquired} acquired, and {missing} missing '
        message += f'{"with" if self.queried else "without"} API query.'
        return message

    def query_api(self, delay=1):
        '''Retrieve files from internet API'''

        # Adjust execution based on settings
        if not settings.get_data['query']:
            return None

        # download data to disk
        for i in self.roster.keys():

            # Don't download if file already downloaded
            if self.roster[i]['found']:
                continue
            
            # Attempt to download
            self.queried = True
            response = requests.get(self.roster[i]['url'])
            if response.status_code == 200:
                self.roster[i]['acquired'] = True
                with open(self.roster[i]['file'], 'wt') as conn:
                    conn.write(response.text)
                    conn.close()
            time.sleep(delay)
        
        return None

###  TEST CODE
if __name__ == '__main__':

    get_data = GetData(
        file_url='input/test_acs_{year}.json',
        api_url='https://api.census.gov/data/{year}/acs/acs5/subject',
        api_query='?get=NAME,S0101_C01_001E&for=county:*',
        print_name='test_census'
    )

    print(get_data)
    response = get_data.query_api()
    print(get_data)

##########==========##########==========##########==========##########==========
