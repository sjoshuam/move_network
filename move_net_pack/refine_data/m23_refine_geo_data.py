'''Remove data defects & derive columns -- census shapefiles'''

##### IMPORT NEEDED CODED

# import settings and utilities
from move_net_pack.m02_define_settings import Settings
from move_net_pack.m03_define_utilities import Utilities
settings = Settings()
utilities = Utilities()

## import predecessor function
from move_net_pack.get_data.m13_get_geo_data import GetGeoData

# import abstract class for refining data
from move_net_pack.refine_data.__init__ import RefineData

## import built-in code
import pickle

# import data processing code and session
import pandas as pd
import geopandas as gpd
from geopy import distance

##### DEFINE CORE CLASS

class RefineGeoData(RefineData):
    '''refine data from census tiger shapefiles'''

    def __init__(self, previous_stage):
        super().__init__(previous_stage)
        self.data = {
            'geo_data':'output/geo_data.pkl',
            'county_distance':'output/county_distance.pkl'
            }

    @staticmethod
    def load_data_mapper(file_urls:list) -> gpd.GeoDataFrame:
        '''proceess each file'''
        dat_list = list()
        for i in file_urls:
            dat_list.append(gpd.read_file(i[1]))
            j = len(dat_list) - 1
            dat_list[j]['year'] = i[0]
        return dat_list

    @staticmethod
    def load_data_reducer(nested_list:list) -> gpd.GeoDataFrame:
        dat = list()
        for i in range(0, len(nested_list)):
            for j in range(0, len(nested_list[i])):
                dat.append(nested_list[i].pop(0))
        dat = pd.concat(dat, axis = 'rows', ignore_index=True)
        return dat

    def remove_defects(self):
        '''remove data defects (types, missing, outliers, etc)'''

        # Evaluate initial status
        assert self.status['load_data'], 'ERROR: Execute load_data() first.'

        # drop unneeded columns and rename
        self.data = self.data[self.data_dict['columns']]
        self.data.columns = self.data_dict['name']

        # convert data types
        dtype_dict = {self.data_dict.loc[i, 'name']:self.data_dict.loc[i, 'type'] for i in self.data_dict.index}
        del dtype_dict['geometry']
        self.data = self.data.astype(dtype_dict)
        self.data.loc[self.data['fips_cbsa'] == 'None', 'fips_cbsa'] = pd.NA

        ## evaluate final status
        self.status['remove_defects'] = True
        print(self)
        return self


    def derive_data(self):
        '''derive needed variables from ingredients -- ids, state usps codes,
        rates, percentages, units, etc...'''

        # confirm that remove_defects was executed
        assert self.status['remove_defects'], 'ERROR: Execute remove_defects() first.'

        # generate ids and set as index
        self.data = self.data.merge(
            right=self.state_dict.drop(columns='name_state'),
            how='left', on='fips_state'
        )
        self.data['id_county'] = self.data['id_state'] +self.data['fips_county']
        self.data = self.data.set_index(['year', 'id_county']).sort_index()

        # rescale surface areas to from km2 to mi2
        self.data['area_land'] = (self.data['area_land'] * 0.38610216).round(1)

        # find unique counties
        self.county_xy = self.data.reset_index().drop_duplicates(
            subset='id_county').copy()[['id_county', 'coords_lat', 'coords_lon']]
        self.county_xy = self.county_xy.set_index('id_county').sort_index()

        # evaluate final status
        self.status['derive_data'] = True
        print(self)

        # export geo data
        url = 'output/geo_data.pkl'
        with open(url, 'wb') as conn:
            pickle.dump(self.data, conn)
            conn.close()
        self.data = {'geo_data':url}

        return self
    
    def distance_mapper(self, county:list) -> pd.DataFrame:
        '''Calculate distance from a specified county'''
        distances = {i:list() for i in county}
        for i in county:
            for j in self.county_xy.index:
                if i < j:
                    dist_iter = round(distance.geodesic(
                        self.county_xy.loc[i],
                        self.county_xy.loc[j],
                        ).miles, 1)
                elif i ==j:
                    dist_iter = 0
                else:
                    dist_iter = pd.NA
                distances[i].append(dist_iter)
            distances[i] = pd.Series(
                distances[i], index=self.county_xy.index, name=i)
        return pd.DataFrame(distances)
        
    def calculate_county_distance(self):
        '''Calculate distances between all US counties'''

        # calculate distances
        distances = utilities.run_in_parallel(
            iterable=self.county_xy.index,
            mapper=self.distance_mapper,
            reducer=lambda x: pd.concat(x, axis='columns'),
            )
        distances = distances[distances.index]

        # write save distance matrix
        url = 'output/county_distance.pkl'
        with open(url, 'wb') as conn:
            pickle.dump(distances, conn)
            conn.close()
        self.data['county_distance'] = url
        
        # evaluate final status
        print('[DISTANCES]\n', distances.iloc[0:5, 0:5])
        return self
    
    def execute(geo_data):
        geo_data.get_data_dict('tiger_dict').load_data().remove_defects()
        geo_data.derive_data().calculate_county_distance()
        return geo_data



##### TEST CODE

if __name__ == '__main__':
    previous_stage = GetGeoData()
    geo_data = RefineGeoData(previous_stage = previous_stage)
    geo_data.execute()


##########==========##########==========##########==========##########==========
